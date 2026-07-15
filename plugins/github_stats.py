import requests
import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/zyp/.env"))

TOOL_NAME = "github_stats"
TOOL_DESCRIPTION = "Get GitHub repo stats, recent commits, or user info"
TOOL_ARGS = {"action": "str: repo, commits, or profile", "target": "str: repo name or username"}

GITHUB_USERNAME = "Tejas13062035"
ZYPHOS_REPO = "ZYPHOS-Z.Y.P.H.OS"

def run(args=None):
    action = args.get("action", "repo") if args else "repo"
    target = args.get("target", ZYPHOS_REPO) if args else ZYPHOS_REPO
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Authorization": f"token {token}"} if token else {}

    if action == "repo":
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USERNAME}/{target}", headers=headers)
        data = r.json()
        result = (
            f"{data.get('full_name', '')}: "
            f"{data.get('description', 'no description')} | "
            f"Stars: {data.get('stargazers_count', 0)} | "
            f"Commits visible via /commits endpoint"
        )
        return {"status": "ok", "result": result}

    elif action == "commits":
        r = requests.get(f"https://api.github.com/repos/{GITHUB_USERNAME}/{target}/commits?per_page=5", headers=headers)
        data = r.json()
        lines = [f"- {c['commit']['message'][:80]}" for c in data[:5]]
        result = "\n".join(lines)
        return {"status": "ok", "result": result}

    elif action == "profile":
        r = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}", headers=headers)
        data = r.json()
        result = (
            f"{data.get('login', '')} — "
            f"Repos: {data.get('public_repos', 0)}, "
            f"Followers: {data.get('followers', 0)}"
        )
        return {"status": "ok", "result": result}

    return {"error": "unknown action"}
