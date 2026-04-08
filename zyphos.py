import sys
import os
from core.smart_planner import smart_plan
from core.smart_executor import smart_execute
from core.daemon import start as daemon_start, stop as daemon_stop, is_running, get_pid
from core.scheduler import schedule_every, schedule_at, launch_background
from core.planner import plan
from core.executor import execute_task
from memory.store import save, recall

def run_goal(goal, smart=False, smart_plan_mode=False):
    print(f"\nGOAL: {goal}")
    tasks = smart_plan(goal) if smart_plan_mode else plan(goal)
    print(f"TASKS: {len(tasks)} generated")
    for task in tasks:
        print(f"  → executing: {task['description']}")
        if smart:
            result = smart_execute(task)
        else:
            result = execute_task(task)
        print(f"  ✓ {result['result']}")
    save(goal, tasks)
    print("MEMORY: saved")

def main():
    if len(sys.argv) < 2:
        print("Usage: python zyphos.py 'goal1' 'goal2' ...")
        return

    if sys.argv[1] == "--status":
        pid = get_pid()
        running = is_running()
        print(f"DAEMON: {'running' if running else 'stopped'} (PID {pid if running else 'none'})")
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

    if sys.argv[1] == "--daemon":
        daemon_start()
        return

    if sys.argv[1] == "--stop":
        daemon_stop()
        return

    if sys.argv[1] == "--restart":
        daemon_stop()
        import time
        time.sleep(1)
        daemon_start()
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

    if sys.argv[1] == "--send":
        goal = " ".join(sys.argv[2:])
        with open(os.path.expanduser("~/zyp/state/pending_goals.txt"), "a") as f:
            f.write(goal + "\n")
        print(f"SENT: {goal}")
        return

    if sys.argv[1] == "--listen":
        from tools.stt import listen
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        print(f"STT: listening for {duration}s...")
        goal = listen(duration)
        print(f"GOAL: {goal}")
        run_goal(goal)
        return

    smart = "--smart" in sys.argv
    smart_plan_mode = "--smart-plan" in sys.argv
    goals = [g for g in sys.argv[1:] if not g.startswith("--")]
    print(f"QUEUE: {len(goals)} goal(s)")
    for goal in goals:
        run_goal(goal, smart=smart, smart_plan_mode=smart_plan_mode)
    
    if "--smart-plan" in sys.argv:
        from core.smart_planner import smart_plan
        from core.smart_executor import smart_execute
        goals = [a for a in sys.argv[1:] if not a.startswith("--")]
        for goal in goals:
            print(f"\nGOAL: {goal}")
            tasks = smart_plan(goal)
            print(f"TASKS: {len(tasks)} generated")
            for task in tasks:
                print(f"  → {task['description']}")
                result = smart_execute(task)
                print(f"  ✓ {result['result']}")
            save(goal, tasks)
        return

if __name__ == "__main__":
    main()
