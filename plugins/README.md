# Zyphos Plugin System

Drop any .py file here to add new tools to Zyphos.

Each plugin file must define:

TOOL_NAME = "my_tool"          # name the LLM will use
TOOL_DESCRIPTION = "do X"     # shown in smart executor system prompt
TOOL_ARGS = {"arg1": "str"}   # expected args

def run(args: dict) -> dict:   # entry point, must return dict with "result" key
    ...
