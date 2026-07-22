import re

TOOL_NAME = "calculator"
TOOL_DESCRIPTION = "evaluates math expressions safely, e.g. '15 * 23 + 7'"
TOOL_ARGS = {"expression": "str"}

ALLOWED_CHARS = re.compile(r'^[\d\s\+\-\*\/\(\)\.\%\*\*]+$')


def run(args: dict) -> dict:
    expr = args.get("expression", "").strip()

    if not expr:
        return {"status": "error", "result": "no expression provided"}

    if not ALLOWED_CHARS.match(expr):
        return {"status": "error", "result": "expression contains disallowed characters"}

    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return {"status": "ok", "result": f"{expr} = {result}"}
    except ZeroDivisionError:
        return {"status": "error", "result": "division by zero"}
    except Exception as e:
        return {"status": "error", "result": f"could not evaluate: {e}"}
