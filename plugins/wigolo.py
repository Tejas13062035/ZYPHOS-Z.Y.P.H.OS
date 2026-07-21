import subprocess
import json

TOOL_NAME = "wigolo"
TOOL_DESCRIPTION = "advanced web search with ML reranking, page fetching, and multi-step research — better than basic search"
TOOL_ARGS = {"action": "str (search|fetch|research)", "query": "str (search query or URL)"}


def _run_wigolo(args_list, timeout=45):
    result = subprocess.run(
        ["wigolo"] + args_list + ["--json"],
        capture_output=True, text=True, timeout=timeout
    )
    # wigolo prints log lines to stderr and JSON to stdout — grab last valid JSON block
    output = result.stdout.strip()
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # try to find the JSON object in case of any leading noise
        start = output.find("{")
        if start != -1:
            try:
                return json.loads(output[start:])
            except json.JSONDecodeError:
                pass
        return {"error": "could not parse wigolo output", "raw": output[:500]}


def run(args: dict) -> dict:
    action = args.get("action", "search")
    query = args.get("query", "")

    if not query:
        return {"status": "error", "result": "no query provided"}

    try:
        if action == "search":
            data = _run_wigolo(["search", query])
            results = data.get("results", [])[:5]
            summary = "\n".join(f"- {r['title']} ({r['url']})" for r in results)
            return {"status": "ok", "result": summary or "no results"}

        elif action == "fetch":
            data = _run_wigolo(["fetch", query], timeout=30)
            content = data.get("content", data.get("markdown", str(data)))
            return {"status": "ok", "result": str(content)[:3000]}

        elif action == "research":
            data = _run_wigolo(["research", query], timeout=90)
            brief = data.get("brief", data.get("summary", str(data)))
            return {"status": "ok", "result": str(brief)[:3000]}

        else:
            return {"status": "error", "result": f"unknown action: {action}"}

    except subprocess.TimeoutExpired:
        return {"status": "error", "result": "wigolo timed out"}
    except Exception as e:
        return {"status": "error", "result": f"wigolo failed: {e}"}
