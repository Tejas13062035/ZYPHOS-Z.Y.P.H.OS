import json
import os
from datetime import datetime

MEMORY_FILE = "state/memory.json"

def load():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save(goal: str, tasks: list):
    memory = load()
    memory.append({
        "timestamp": datetime.now().isoformat(),
        "goal": goal,
        "tasks": tasks
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def recall(n: int = 5):
    return load()[-n:]
