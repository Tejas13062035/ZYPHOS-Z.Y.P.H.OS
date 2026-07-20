import subprocess
import json

TOOL_NAME = "webintel"
TOOL_DESCRIPTION = "advanced web intelligence: read any webpage, get YouTube transcripts, semantic search, RSS feeds"
TOOL_ARGS = {"action": "str (read_page|youtube_transcript|semantic_search|rss)", "target": "str (URL or query)"}


def run(args: dict) -> dict:
    action = args.get("action", "read_page")
    target = args.get("target", "")

    if not target:
        return {"status": "error", "result": "no target provided"}

    try:
        if action == "read_page":
            result = subprocess.run(
                ["curl", "-s", f"https://r.jina.ai/{target}"],
                capture_output=True, text=True, timeout=30
            )
            return {"status": "ok", "result": result.stdout[:3000]}

        elif action == "youtube_transcript":
            result = subprocess.run(
                ["yt-dlp", "--write-sub", "--skip-download", "--sub-lang", "en", "-o", "/tmp/%(id)s", target],
                capture_output=True, text=True, timeout=60
            )
            return {"status": "ok", "result": result.stdout[:2000]}

        elif action == "semantic_search":
            result = subprocess.run(
                ["mcporter", "call", f'exa.web_search_exa(query: "{target}")'],
                capture_output=True, text=True, timeout=30
            )
            return {"status": "ok", "result": result.stdout[:3000]}

        elif action == "rss":
            import feedparser
            feed = feedparser.parse(target)
            entries = [f"{e.title} — {e.link}" for e in feed.entries[:5]]
            return {"status": "ok", "result": "\n".join(entries)}

        else:
            return {"status": "error", "result": f"unknown action: {action}"}

    except Exception as e:
        return {"status": "error", "result": f"webintel failed: {e}"}
