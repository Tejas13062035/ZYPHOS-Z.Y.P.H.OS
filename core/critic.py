import json
from core.llm import ask

CRITIC_PROMPT = """You are a task critic for an AI agent called Zyphos.
You are given a task description and the result it produced.
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

def critique(task: str, result: str) -> dict:
    prompt = f"Task: {task}\nResult: {result}"
    response = ask(prompt, system=CRITIC_PROMPT, max_tokens=200)
    return _extract_json(response)
