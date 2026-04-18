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

        elif word == "scroll" and i + 2 < len(words):
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"scroll {words[i+1]} {words[i+2]}",
                "status": "pending",
                "result": None
            })
            i += 3

        elif word == "drag" and i + 4 < len(words):
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"drag {words[i+1]} {words[i+2]} {words[i+3]} {words[i+4]}",
                "status": "pending",
                "result": None
            })
            i += 5

        elif word == "hotkey":
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"hotkey {' '.join(words[i+1:])}",
                "status": "pending",
                "result": None
            })
        elif word == "search" and i + 1 < len(words):
            query = " ".join(words[i+1:])
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"search {query}",
                "status": "pending",
                "result": None
            })
            break

        elif word == "play" and i + 1 < len(words):
            query = " ".join(words[i+1:])
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"play {query}",
                "status": "pending",
                "result": None
            })
            break

        elif word == "stop":
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": "stop music",
                "status": "pending",
                "result": None
            })
            i += 1

        elif word == "open":
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"open {' '.join(words[i+1:])}",
                "status": "pending",
                "result": None
            })
            break

        elif word == "network" or word == "scan":
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"network scan",
                "status": "pending",
                "result": None
            })
            break

        elif word == "speak" or word == "say":
            text = " ".join(words[i+1:])
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"speak {text}",
                "status": "pending",
                "result": None
            })
            break

        elif word == "write" and i + 1 < len(words):
            text = " ".join(words[i+1:])
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "description": f"type {text}",
                "status": "pending",
                "result": None
            })
            break

        else:
            i += 1
    return tasks
