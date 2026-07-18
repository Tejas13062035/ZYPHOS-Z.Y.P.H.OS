import requests
import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/zyp/.env"))

TOOL_NAME = "github_stats"
TOOL_DESCRIPTION = "Get GitHub repo stats, recent commits, or user info for ANY public repo or user"
TOOL_ARGS = {
    "action": "str: repo, commits, or profile",
    "owner": "str: GitHub username/org (default: Tejas13062035)",
    "target": "str: repo name or username"
}

DEFAULT_OWNER = "Tejas13062035"
DEFAULT_REPO = "Zyphos"

def run(args=None):
    action = args.get("action", "repo") if args else "repo"
    owner = args.get("owner", DEFAULT_OWNER) if args else DEFAULT_OWNER
    target = args.get("target", DEFAULT_REPO) if args else DEFAULT_REPO
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Authorization": f"token {token}"} if token else {}

    try:
        if action == "repo":
            r = requests.get(f"https://api.github.com/repos/{owner}/{target}", headers=headers)
            data = r.json()
            if "message" in data and "full_name" not in data:
                return {"error": data["message"]}
            result = (
                f"{data.get('full_name', '')}: "
                f"{data.get('description', 'no description')} | "
                f"Stars: {data.get('stargazers_count', 0)} | "
                f"Forks: {data.get('forks_count', 0)} | "
                f"Language: {data.get('language', 'unknown')}"
            )
            return {"status": "ok", "result": result}

        elif action == "commits":
            r = requests.get(f"https://api.github.com/repos/{owner}/{target}/commits?per_page=5", headers=headers)
            data = r.json()
            if isinstance(data, list):
                lines = [f"- {c['commit']['message'][:80]}" for c in data[:5]]
                result = "\n".join(lines)
            else:
                result = str(data.get("message", "unexpected response"))
            return {"status": "ok", "result": result}

        elif action == "profile":
            username = target if target != DEFAULT_REPO else owner
            r = requests.get(f"https://api.github.com/users/{username}", headers=headers)
            data = r.json()
            if "message" in data and "login" not in data:
                return {"error": data["message"]}
            result = (
                f"{data.get('login', '')} — "
                f"Repos: {data.get('public_repos', 0)}, "
                f"Followers: {data.get('followers', 0)}, "
                f"Bio: {data.get('bio', 'none')}"
            )
            return {"status": "ok", "result": result}

        return {"error": "unknown action"}
    except Exception as e:
        return {"error": str(e)}
