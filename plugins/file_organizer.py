import os
import shutil

TOOL_NAME = "file_organizer"
TOOL_DESCRIPTION = "Organize files in a folder by type into subfolders"
TOOL_ARGS = {"path": "folder path to organize e.g. /mnt/c/Users/HP/Downloads"}

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".sh", ".bat"],
    "Executables": [".exe", ".msi", ".apk", ".dmg"],
    "Others": []
}

def get_category(ext: str) -> str:
    for category, extensions in CATEGORIES.items():
        if ext.lower() in extensions:
            return category
    return "Others"

def run(args: dict) -> dict:
    path = args.get("path", "/mnt/c/Users/HP/Downloads")
    path = os.path.expanduser(path)

    if not os.path.exists(path):
        return {"error": f"path not found: {path}"}

    moved = {}
    errors = []

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            continue

        ext = os.path.splitext(filename)[1]
        category = get_category(ext)

        dest_dir = os.path.join(path, category)
        os.makedirs(dest_dir, exist_ok=True)

        try:
            shutil.move(filepath, os.path.join(dest_dir, filename))
            moved[category] = moved.get(category, 0) + 1
        except Exception as e:
            errors.append(f"{filename}: {e}")

    summary = ", ".join([f"{v} {k}" for k, v in moved.items()])
    return {
        "status": "ok",
        "moved": moved,
        "summary": f"Organized: {summary}" if summary else "Nothing to organize",
        "errors": errors
    }
