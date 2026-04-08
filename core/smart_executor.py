import json
from tools.vision import look
from core.llm import ask
from tools.sidecar import click, type_text, screenshot, scroll, drag, hotkey
from tools.filesystem import read_file, write_file, list_dir, delete_file
from tools.shell import run_shell

SYSTEM_PROMPT = """You are a task execution engine. Given a task description, respond with a JSON object only.
No explanation, no markdown, just raw JSON.

Available tools:
- look: {"prompt": str}  — takes a screenshot and describes what's on screen
- screenshot: {} 
- click: {"x": int, "y": int}
- type_text: {"text": str}
- scroll: {"x": int, "y": int, "amount": int}
- drag: {"x1": int, "y1": int, "x2": int, "y2": int}
- hotkey: {"keys": [str]}
- read_file: {"path": str}
- write_file: {"path": str, "content": str}
- list_dir: {"path": str}
- delete_file: {"path": str}
- run_shell: {"command": str}

Respond with exactly: {"tool": "tool_name", "args": {...}}"""

TOOL_MAP = {
    "look": lambda args: look(args.get("prompt", "What do you see on this screen?")),
    "screenshot": lambda args: screenshot(),
    "click": lambda args: click(args["x"], args["y"]),
    "type_text": lambda args: type_text(args["text"]),
    "scroll": lambda args: scroll(args["x"], args["y"], args.get("amount", 3)),
    "drag": lambda args: drag(args["x1"], args["y1"], args["x2"], args["y2"]),
    "hotkey": lambda args: hotkey(args["keys"]),
    "read_file": lambda args: read_file(args["path"]),
    "write_file": lambda args: write_file(args["path"], args["content"]),
    "list_dir": lambda args: list_dir(args["path"]),
    "delete_file": lambda args: delete_file(args["path"]),
    "run_shell": lambda args: run_shell(args["command"]),
}

def smart_execute(task: dict) -> dict:
    desc = task.get("description", "")
    response = ask(desc, system=SYSTEM_PROMPT, max_tokens=100)

    try:
        # extract first complete JSON object
        start = response.find("{")
        depth = 0
        end = start
        for i, c in enumerate(response[start:], start):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        clean = response[start:end]
        parsed = json.loads(clean)
        tool = parsed["tool"]
        args = parsed.get("args", {})

        if tool not in TOOL_MAP:
            task["status"] = "done"
            task["result"] = {"error": f"unknown tool: {tool}"}
            return task

        result = TOOL_MAP[tool](args)
        task["status"] = "done"
        task["result"] = result
    except Exception as e:
        task["status"] = "done"
        task["result"] = {"error": f"smart_execute failed: {e}", "raw": response}

    return task
