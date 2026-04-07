import sys
from core.planner import plan
from core.executor import execute_task
from memory.store import save, recall

def main():
    if len(sys.argv) < 2:
        print("Usage: python zyphos.py 'your goal'")
        return

    goal = " ".join(sys.argv[1:])
    print(f"GOAL: {goal}")

    tasks = plan(goal)
    print(f"TASKS: {len(tasks)} generated")

    for task in tasks:
        print(f"  → executing: {task['description']}")
        result = execute_task(task)
        print(f"  ✓ {result['result']}")

    save(goal, tasks)
    print("MEMORY: saved")

if __name__ == "__main__":
    main()
