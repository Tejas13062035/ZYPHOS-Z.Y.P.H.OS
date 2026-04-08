import os

def read_file(path: str) -> dict:
    try:
        with open(os.path.expanduser(path), "r") as f:
            return {"status": "ok", "content": f.read()}
    except Exception as e:
        return {"error": str(e)}

def write_file(path: str, content: str) -> dict:
    try:
        with open(os.path.expanduser(path), "w") as f:
            f.write(content)
        return {"status": "written", "path": path}
    except Exception as e:
        return {"error": str(e)}

def list_dir(path: str) -> dict:
    try:
        entries = os.listdir(os.path.expanduser(path))
        return {"status": "ok", "entries": entries}
    except Exception as e:
        return {"error": str(e)}

def delete_file(path: str) -> dict:
    try:
        os.remove(os.path.expanduser(path))
        return {"status": "deleted", "path": path}
    except Exception as e:
        return {"error": str(e)}
