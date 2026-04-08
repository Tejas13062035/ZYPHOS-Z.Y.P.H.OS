import time
import os
import sys
import signal
from datetime import datetime
from core.planner import plan
from core.executor import execute_task
from memory.store import save

GOAL_FILE = os.path.expanduser("~/zyp/state/pending_goals.txt")
LOG_FILE = os.path.expanduser("~/zyp/logs/daemon.log")
PID_FILE = os.path.expanduser("~/zyp/state/zyphos.pid")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def write_pid():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def clear_pid():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def get_pid():
    if not os.path.exists(PID_FILE):
        return None
    with open(PID_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except ValueError:
            return None

def is_running():
    pid = get_pid()
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False

def stop():
    pid = get_pid()
    if pid is None:
        print("DAEMON: not running (no PID file)")
        return
    if not is_running():
        print("DAEMON: not running (stale PID)")
        clear_pid()
        return
    os.kill(pid, signal.SIGTERM)
    clear_pid()
    print(f"DAEMON: stopped (PID {pid})")

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
    if is_running():
        print(f"DAEMON: already running (PID {get_pid()})")
        return
    write_pid()
    log(f"DAEMON: started (PID {os.getpid()})")
    open(GOAL_FILE, "a").close()

    def handle_exit(signum, frame):
        log("DAEMON: shutting down")
        clear_pid()
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    while True:
        with open(GOAL_FILE, "r") as f:
            goals = [g.strip() for g in f.readlines() if g.strip()]
        if goals:
            with open(GOAL_FILE, "w") as f:
                f.write("")
            for goal in goals:
                run_goal(goal)
        time.sleep(2)

if __name__ == "__main__":
    start()
