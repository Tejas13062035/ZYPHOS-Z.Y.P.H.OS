import os
import pickle
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOOL_NAME = "gmail"
TOOL_DESCRIPTION = "Send and read emails via Gmail. Actions: send, read, search"
TOOL_ARGS = {
    "action": "send|read|search",
    "to": "recipient email (for send)",
    "subject": "email subject (for send)",
    "body": "email body (for send)",
    "query": "search query (for search)"
}

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly"
]
CREDS_FILE = os.path.expanduser("~/zyp/state/credentials.json")
TOKEN_FILE = os.path.expanduser("~/zyp/state/gmail_token.pickle")

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob"
            )
            auth_url, _ = flow.authorization_url(
                access_type="offline",
                prompt="consent"
            )
            print(f"\nOpen this URL in your browser:\n{auth_url}\n")
            code = input("Paste the authorization code: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build("gmail", "v1", credentials=creds)

def run(args: dict) -> dict:
    action = args.get("action", "read").lower()
    try:
        service = get_service()

        if action == "send":
            to = args.get("to", "")
            subject = args.get("subject", "")
            body = args.get("body", "")
            if not to:
                return {"error": "recipient email required"}
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            sent = service.users().messages().send(
                userId="me",
                body={"raw": raw}
            ).execute()
            return {"status": "sent", "id": sent["id"]}

        elif action == "read":
            results = service.users().messages().list(
                userId="me", maxResults=5, labelIds=["INBOX"]
            ).execute()
            messages = results.get("messages", [])
            emails = []
            for m in messages:
                msg = service.users().messages().get(
                    userId="me", id=m["id"], format="metadata",
                    metadataHeaders=["From", "Subject", "Date"]
                ).execute()
                headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
                emails.append({
                    "from": headers.get("From", ""),
                    "subject": headers.get("Subject", ""),
                    "date": headers.get("Date", "")
                })
            return {"status": "ok", "emails": emails}

        elif action == "search":
            query = args.get("query", "")
            results = service.users().messages().list(
                userId="me", q=query, maxResults=5
            ).execute()
            messages = results.get("messages", [])
            emails = []
            for m in messages:
                msg = service.users().messages().get(
                    userId="me", id=m["id"], format="metadata",
                    metadataHeaders=["From", "Subject", "Date"]
                ).execute()
                headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
                emails.append({
                    "from": headers.get("From", ""),
                    "subject": headers.get("Subject", ""),
                    "date": headers.get("Date", "")
                })
            return {"status": "ok", "emails": emails}

        else:
            return {"error": f"unknown action: {action}"}

    except Exception as e:
        return {"error": str(e)}
