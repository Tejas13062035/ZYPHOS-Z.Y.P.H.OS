TOOL_NAME = "hello"
TOOL_DESCRIPTION = "says hello to a person by name"
TOOL_ARGS = {"name": "str"}

def run(args: dict) -> dict:
    name = args.get("name", "world")
    return {"result": f"Hello, {name}!"}
