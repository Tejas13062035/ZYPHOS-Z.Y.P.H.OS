import time
import os
import sys
import subprocess
from datetime import datetime

INTERVAL = 30  # seconds between checks
LOG_FILE = os.path.expanduser("~/zyp/logs/watchdog.log")
VENV_PYTHON = os.path.expanduser("~/zyp/venv/bin/python")
ZYPHOS_DIR = os.path.expanduser("~/zyp")


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def is_daemon_running():
    pid_file = os.path.expanduser("~/zyp/state/zyphos.pid")
    if not os.path.exists(pid_file):
        return False
    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return True
    except (ValueError, ProcessLookupError, OSError):
        return False


def restart_daemon():
    log("WATCHDOG: daemon down — restarting...")
    subprocess.Popen(
        [VENV_PYTHON, "zyphos.py", "--daemon"],
        cwd=ZYPHOS_DIR,
        stdout=open(os.path.expanduser("~/zyp/logs/daemon.log"), "a"),
        stderr=subprocess.STDOUT
    )
    log("WATCHDOG: daemon restarted")


def main():
    log(f"WATCHDOG: started (PID {os.getpid()}) — checking every {INTERVAL}s")
    while True:
        if not is_daemon_running():
            restart_daemon()
        else:
            log("WATCHDOG: daemon OK")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
