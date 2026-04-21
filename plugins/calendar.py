import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

TOOL_NAME = "calendar"
TOOL_DESCRIPTION = "Manage Google Calendar: list upcoming events, add new events, check today's schedule"
TOOL_ARGS = {"action": "list|add|today", "summary": "event title (for add)", "date": "YYYY-MM-DD (for add)", "time": "HH:MM (for add)"}

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDS_FILE = os.path.expanduser("~/zyp/state/credentials.json")
TOKEN_FILE = os.path.expanduser("~/zyp/state/token.pickle")

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
    return build("calendar", "v3", credentials=creds)

def run(args: dict) -> dict:
    action = args.get("action", "list").lower()
    try:
        service = get_service()

        if action in ["list", "today"]:
            now = datetime.datetime.utcnow()
            if action == "today":
                end = now.replace(hour=23, minute=59, second=59)
            else:
                end = now + datetime.timedelta(days=7)
            events_result = service.events().list(
                calendarId="primary",
                timeMin=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                timeMax=end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                maxResults=10,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            events = events_result.get("items", [])
            if not events:
                return {"status": "no events found"}
            result = []
            for e in events:
                start = e["start"].get("dateTime", e["start"].get("date"))
                result.append(f"{start}: {e['summary']}")
            return {"status": "ok", "events": result}

        elif action == "add":
            summary = args.get("summary", "Untitled")
            date = args.get("date", datetime.date.today().isoformat())
            time = args.get("time", "09:00")
            start_dt = f"{date}T{time}:00"
            end_dt = f"{date}T{str(int(time[:2])+1).zfill(2)}{time[2:]}:00"
            event = {
                "summary": summary,
                "start": {"dateTime": start_dt, "timeZone": "Asia/Kolkata"},
                "end": {"dateTime": end_dt, "timeZone": "Asia/Kolkata"},
            }
            created = service.events().insert(calendarId="primary", body=event).execute()
            return {"status": "created", "event": created.get("summary"), "link": created.get("htmlLink")}

        else:
            return {"error": f"unknown action: {action}"}

    except Exception as e:
        return {"error": str(e)}
