import json
import os

MEMORY_FILE = os.path.expanduser("~/zyp/state/memory.json")
OUTPUT_FILE = os.path.expanduser("~/zyp/state/training_data.jsonl")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        print("No memory file found.")
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def format_entry(entry):
    goal = entry.get("goal", "")
    tasks = entry.get("tasks", [])
    if not goal or not tasks:
        return None

    # format as instruction → output pairs
    pairs = []

    # goal → task list
    task_list = [t.get("description", "") for t in tasks if t.get("description")]
    if task_list:
        pairs.append({
            "instruction": goal,
            "output": json.dumps([{"description": t} for t in task_list])
        })

    # each task → tool call
    for task in tasks:
        desc = task.get("description", "")
        result = task.get("result", "")
        if desc and result:
            pairs.append({
                "instruction": desc,
                "output": str(result)
            })

    return pairs

def collect():
    memory = load_memory()
    print(f"Loaded {len(memory)} memory entries")

    total = 0
    with open(OUTPUT_FILE, "w") as out:
        for entry in memory:
            pairs = format_entry(entry)
            if not pairs:
                continue
            for pair in pairs:
                out.write(json.dumps(pair) + "\n")
                total += 1

    print(f"Training data collected: {total} pairs")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    collect()
