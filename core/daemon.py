import time
import os
import sys
from datetime import datetime
from core.planner import plan
from core.executor import execute_task
from memory.store import save

GOAL_FILE = os.path.expanduser("~/zyp/state/pending_goals.txt")
LOG_FILE = os.path.expanduser("~/zyp/logs/daemon.log")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_goal(goal):
    log(f"GOAL: {goal}")
    tasks = plan(goal)
    log(f"TASKS: {len(tasks)} generated")
    for task in tasks:
        log(f"  → {task['description']}")
        result = execute_task(task)
        log(f"  ✓ {result['result']}")
    save(goal, tasks)

def start():
    log("DAEMON: started")
    open(GOAL_FILE, "a").close()  # ensure file exists
    while True:
        with open(GOAL_FILE, "r") as f:
            goals = [g.strip() for g in f.readlines() if g.strip()]
        if goals:
            with open(GOAL_FILE, "w") as f:
                f.write("")  # clear queue
            for goal in goals:
                run_goal(goal)
        time.sleep(2)

if __name__ == "__main__":
    start()
