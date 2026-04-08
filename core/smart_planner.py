import uuid
import json
from core.llm import ask

SYSTEM_PROMPT = """You are a computer task planner. Output ONLY a JSON array. No comments. No explanation.

Rules:
- Every item must have ONLY a "description" key
- Use exact formats below, nothing else

Allowed descriptions:
- "screenshot"
- "click 500 300"
- "type hello world"
- "scroll 500 500"
- "hotkey ctrl s"
- "run_shell ls"

Bad output (never do this):
[{"action": "click"}]
[{"description": "click", "x": 500}]

Good output:
[{"description": "screenshot"}, {"description": "click 960 540"}]

Output the JSON array now:"""

def extract_json(text: str):
    start = text.find("[")
    if start == -1:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None

def smart_plan(goal: str) -> list:
    prompt = f"Goal: {goal}"
    response = ask(prompt, system=SYSTEM_PROMPT, max_tokens=500)

    raw = extract_json(response)
    if not raw:
        print(f"PLANNER: failed to parse LLM response:\n{response}")
        return []

    try:
        tasks = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"PLANNER: JSON error: {e}")
        return []

    return [
        {
            "id": str(uuid.uuid4())[:8],
            "description": t.get("description", ""),
            "status": "pending",
            "result": None
        }
        for t in tasks if "description" in t
    ]
