import os
import json
from datetime import datetime

TOOL_NAME = "notes"
TOOL_DESCRIPTION = "Add, read, list or delete personal notes"
TOOL_ARGS = {"action": "add|read|list|delete", "note": "note text (for add)", "title": "note title"}

NOTES_FILE = os.path.expanduser("~/zyp/state/notes.json")

def load():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE) as f:
        return json.load(f)

def save(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def run(args: dict) -> dict:
    action = args.get("action", "list").lower()
    
    if action == "add":
        note = args.get("note", args.get("text", ""))
        title = args.get("title", note[:30] + "..." if len(note) > 30 else note)
        if not note:
            return {"error": "note text required"}
        notes = load()
        notes.append({
            "id": len(notes) + 1,
            "title": title,
            "note": note,
            "timestamp": datetime.now().isoformat()
        })
        save(notes)
        return {"status": "saved", "title": title}

    elif action == "list":
        notes = load()
        if not notes:
            return {"status": "no notes found"}
        return {"status": "ok", "notes": [f"{n['id']}. {n['title']} ({n['timestamp'][:10]})" for n in notes]}

    elif action == "read":
        title = args.get("title", "").lower()
        query = args.get("query", title)
        notes = load()
        matches = [n for n in notes if query.lower() in n["title"].lower() or query.lower() in n["note"].lower()]
        if not matches:
            return {"status": "no matching notes"}
        return {"status": "ok", "notes": [{"title": n["title"], "note": n["note"]} for n in matches]}

    elif action == "delete":
        note_id = int(args.get("id", 0))
        notes = load()
        notes = [n for n in notes if n["id"] != note_id]
        save(notes)
        return {"status": "deleted", "id": note_id}

    return {"error": f"unknown action: {action}"}
