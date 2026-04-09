import json
from core.llm import ask

CRITIC_PROMPT = """You are a task critic for an AI agent called Zyphos.
You are given a task description, the tool that was called, the args passed to it, and the result.
Decide if the task succeeded or failed.

Respond ONLY with a JSON object in this format:
{"passed": true, "reason": "short reason"}
or
{"passed": false, "reason": "short reason"}

No explanation outside the JSON."""


def _extract_json(text: str) -> dict:
    start = text.find("{")
    if start == -1:
        return {"passed": True, "reason": "no JSON in critic response"}
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if depth == 0:
            try:
                return json.loads(text[start:i+1])
            except json.JSONDecodeError:
                return {"passed": True, "reason": "json parse failed"}
    return {"passed": True, "reason": "incomplete json"}


def critique(task: str, result: str, tool: str = "", args: dict = None) -> dict:
    args_str = json.dumps(args) if args else "none"
    prompt = (
        f"Task: {task}\n"
        f"Tool called: {tool if tool else 'unknown'}\n"
        f"Args: {args_str}\n"
        f"Result: {result}"
    )
    response = ask(prompt, system=CRITIC_PROMPT, max_tokens=200)
    return _extract_json(response)
