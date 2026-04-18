import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

TOOL_NAME = "drive"
TOOL_DESCRIPTION = "Manage Google Drive. Actions: list, upload, download, search"
TOOL_ARGS = {
    "action": "list|upload|download|search",
    "query": "search query (for search)",
    "file_path": "local file path (for upload)",
    "file_name": "file name on Drive (for download)",
    "save_path": "local path to save (for download)"
}

SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDS_FILE = os.path.expanduser("~/zyp/state/credentials.json")
TOKEN_FILE = os.path.expanduser("~/zyp/state/drive_token.pickle")

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
    return build("drive", "v3", credentials=creds)

def run(args: dict) -> dict:
    action = args.get("action", "list").lower()
    try:
        service = get_service()

        if action == "list":
            results = service.files().list(
                pageSize=10,
                fields="files(id, name, mimeType, modifiedTime)"
            ).execute()
            files = results.get("files", [])
            return {"status": "ok", "files": [{"name": f["name"], "type": f["mimeType"], "modified": f["modifiedTime"]} for f in files]}

        elif action == "search":
            query = args.get("query", "")
            results = service.files().list(
                q=f"name contains '{query}'",
                pageSize=10,
                fields="files(id, name, mimeType, modifiedTime)"
            ).execute()
            files = results.get("files", [])
            return {"status": "ok", "files": [{"name": f["name"], "id": f["id"]} for f in files]}

        elif action == "upload":
            file_path = args.get("file_path", "")
            if not os.path.exists(file_path):
                return {"error": f"file not found: {file_path}"}
            file_name = os.path.basename(file_path)
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(
                body={"name": file_name},
                media_body=media,
                fields="id, name"
            ).execute()
            return {"status": "uploaded", "name": file["name"], "id": file["id"]}

        elif action == "download":
            query = args.get("query", "")
            save_path = args.get("save_path", os.path.expanduser("~/zyp/downloads/"))
            os.makedirs(save_path, exist_ok=True)
            results = service.files().list(
                q=f"name contains '{query}'",
                pageSize=1,
                fields="files(id, name)"
            ).execute()
            files = results.get("files", [])
            if not files:
                return {"error": f"no file found matching: {query}"}
            f = files[0]
            request = service.files().get_media(fileId=f["id"])
            path = os.path.join(save_path, f["name"])
            with open(path, "wb") as out:
                downloader = MediaIoBaseDownload(out, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
            return {"status": "downloaded", "name": f["name"], "path": path}

        else:
            return {"error": f"unknown action: {action}"}

    except Exception as e:
        return {"error": str(e)}
