import json
from core.llm import ask

CHAINER_PROMPT = """You are a goal chaining engine for an AI agent called Zyphos.
You are given the original goal and the result of the last action taken.
Decide if the goal is fully complete, or if another action is needed.

Respond ONLY with a JSON object in one of these two formats:

If done:
{"done": true, "reason": "short reason"}

If another action is needed:
{"done": false, "next": "description of next action to take"}

No explanation outside the JSON."""


def _extract_json(text: str) -> dict:
    start = text.find("{")
    if start == -1:
        return {"done": True, "reason": "no JSON in chainer response"}
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
                return {"done": True, "reason": "json parse failed"}
    return {"done": True, "reason": "incomplete json"}


def chain(original_goal: str, last_result: str, max_steps: int = 5) -> list:
    """
    Runs a goal chaining loop. Returns list of all steps taken.
    Each step: {"action": str, "result": str}
    """
    from core.smart_executor import smart_execute_with_critique

    steps = []
    current_action = original_goal
    current_result = last_result

    for step in range(max_steps):
        prompt = f"Original goal: {original_goal}\nLast action: {current_action}\nLast result: {current_result}"
        response = ask(prompt, system=CHAINER_PROMPT, max_tokens=200)
        verdict = _extract_json(response)

        if verdict.get("done"):
            reason = verdict.get("reason", "complete")
            print(f"[CHAIN] Done after {step+1} step(s): {reason}")
            break

        next_action = verdict.get("next", "")
        if not next_action:
            print(f"[CHAIN] No next action returned, stopping.")
            break

        print(f"[CHAIN] Step {step+2}: {next_action}")
        task = {"description": next_action}
        result = smart_execute_with_critique(task)
        steps.append({"action": next_action, "result": result.get("result", "")})
        current_action = next_action
        current_result = result.get("result", "")

    return steps
