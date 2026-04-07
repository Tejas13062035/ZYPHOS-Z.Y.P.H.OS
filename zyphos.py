import sys
import os
from core.daemon import start as daemon_start
from core.scheduler import schedule_every, schedule_at, launch_background
from core.planner import plan
from core.executor import execute_task
from memory.store import save, recall

def run_goal(goal):
    print(f"\nGOAL: {goal}")
    tasks = plan(goal)
    print(f"TASKS: {len(tasks)} generated")
    for task in tasks:
        print(f"  → executing: {task['description']}")
        result = execute_task(task)
        print(f"  ✓ {result['result']}")
    save(goal, tasks)
    print("MEMORY: saved")

def main():
    if len(sys.argv) < 2:
        print("Usage: python zyphos.py 'goal1' 'goal2' ...")
        return

    if sys.argv[1] == "--status":
        print("STATUS: online")
        entries = recall(5)
        print(f"LAST {len(entries)} goals:")
        for e in entries:
            print(f"  [{e['timestamp']}] {e['goal']}")
        return

    if sys.argv[1] == "--memory":
        query = " ".join(sys.argv[2:])
        entries = recall(10)
        print(f"MEMORY RECALL: {query}")
        for e in entries:
            print(f"  [{e['timestamp']}] {e['goal']}")
        return

    if sys.argv[1] == "--schedule":
        goal = sys.argv[2]
        every = None
        at = None
        bg = "--bg" in sys.argv
        if "--every" in sys.argv:
            every = int(sys.argv[sys.argv.index("--every") + 1])
        if "--at" in sys.argv:
            at = sys.argv[sys.argv.index("--at") + 1]
        if bg:
            launch_background(goal, every=every, at=at)
        elif every:
            schedule_every(goal, every)
        elif at:
            schedule_at(goal, at)
        else:
            print("ERROR: --schedule needs --every SECONDS or --at HH:MM")
        return

    if sys.argv[1] == "--daemon":
        daemon_start()
        return

    if sys.argv[1] == "--send":
        goal = " ".join(sys.argv[2:])
        with open(os.path.expanduser("~/zyp/state/pending_goals.txt"), "a") as f:
            f.write(goal + "\n")
        print(f"SENT: {goal}")
        return

    goals = sys.argv[1:]
    print(f"QUEUE: {len(goals)} goal(s)")
    for goal in goals:
        run_goal(goal)

if __name__ == "__main__":
    main()
