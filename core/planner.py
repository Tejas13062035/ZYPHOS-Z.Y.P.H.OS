import uuid

def plan(goal: str) -> list:
    words = goal.lower().split()
    tasks = []
    i = 0
    while i < len(words):
        word = words[i]
        if word == "click" and i + 2 < len(words):
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"click {words[i+1]} {words[i+2]}",
                "status": "pending",
                "result": None
            })
            i += 3
        elif word == "type" and i + 1 < len(words):
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"type {' '.join(words[i+1:])}",
                "status": "pending",
                "result": None
            })
            break
        elif word == "screenshot":
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": "screenshot",
                "status": "pending",
                "result": None
            })
            i += 1
        else:
            i += 1
    return tasks
