from tools.sidecar import click, type_text, screenshot

def execute_task(task: dict) -> dict:
    desc = task.get("description", "").lower()
    result = None

    if "click" in desc:
        parts = desc.split()
        try:
            x = int(parts[parts.index("click") + 1])
            y = int(parts[parts.index("click") + 2])
            result = click(x, y)
        except (ValueError, IndexError):
            result = {"error": "click requires x y coordinates"}

    elif "type" in desc:
        parts = desc.split("type ", 1)
        text = parts[1] if len(parts) > 1 else ""
        result = type_text(text)

    elif "screenshot" in desc:
        result = screenshot()
        result = {"status": "screenshot taken", "has_image": "image" in result}

    else:
        result = {"error": f"unknown task: {desc}"}

    task["status"] = "done"
    task["result"] = result
    return task
