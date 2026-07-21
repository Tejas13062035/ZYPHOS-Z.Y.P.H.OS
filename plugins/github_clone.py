import subprocess
import os
import requests

TOOL_NAME = "github_clone"
TOOL_DESCRIPTION = "Clone a GitHub repo or download it as a zip"
TOOL_ARGS = {
    "action": "str: clone or download",
    "owner": "str: GitHub username/org",
    "repo": "str: repo name",
    "path": "str (optional): where to save, defaults to ~/downloads"
}

DEFAULT_PATH = os.path.expanduser("~/downloads")

def run(args=None):
    action = args.get("action", "clone") if args else "clone"
    owner = args.get("owner", "") if args else ""
    repo = args.get("repo", "") if args else ""
    path = args.get("path", DEFAULT_PATH) if args else DEFAULT_PATH

    if not owner or not repo:
        return {"error": "owner and repo are required"}

    os.makedirs(path, exist_ok=True)

    if action == "clone":
        try:
            target_dir = os.path.join(path, repo)
            result = subprocess.run(
                ["git", "clone", f"https://github.com/{owner}/{repo}.git", target_dir],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                return {"status": "ok", "result": f"Cloned {owner}/{repo} to {target_dir}"}
            else:
                return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}

    elif action == "download":
        try:
            url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
            zip_path = os.path.join(path, f"{repo}.zip")
            r = requests.get(url, timeout=60)
            if r.status_code != 200:
                # try master branch if main doesn't exist
                url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
                r = requests.get(url, timeout=60)
            if r.status_code == 200:
                with open(zip_path, "wb") as f:
                    f.write(r.content)
                return {"status": "ok", "result": f"Downloaded {owner}/{repo} to {zip_path}"}
            else:
                return {"error": f"Failed to download, status {r.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "unknown action, use 'clone' or 'download'"}
