import time
import subprocess
import sys
from datetime import datetime
from core.planner import plan
from core.executor import execute_task
from memory.store import save

def run_goal(goal):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] GOAL: {goal}")
    tasks = plan(goal)
    print(f"TASKS: {len(tasks)} generated")
    for task in tasks:
        print(f"  → executing: {task['description']}")
        result = execute_task(task)
        print(f"  ✓ {result['result']}")
    save(goal, tasks)

def schedule_every(goal, seconds):
    print(f"SCHEDULER: '{goal}' every {seconds}s — Ctrl+C to stop")
    while True:
        run_goal(goal)
        time.sleep(seconds)

def schedule_at(goal, time_str):
    print(f"SCHEDULER: '{goal}' at {time_str}")
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == time_str:
            run_goal(goal)
            time.sleep(60)  # prevent double-trigger within same minute
        time.sleep(10)

def launch_background(goal, every=None, at=None):
    args = [sys.executable, "zyphos.py", "--schedule", goal]
    if every:
        args += ["--every", str(every)]
    if at:
        args += ["--at", at]
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"SCHEDULER: running in background (PID {proc.pid})")
