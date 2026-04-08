import time
import os
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from core.daemon import is_running, get_pid
from memory.store import recall

GOAL_FILE = os.path.expanduser("~/zyp/state/pending_goals.txt")
LOG_FILE = os.path.expanduser("~/zyp/logs/daemon.log")

console = Console()

def get_pending():
    if not os.path.exists(GOAL_FILE):
        return []
    with open(GOAL_FILE, "r") as f:
        return [g.strip() for g in f.readlines() if g.strip()]

def get_last_logs(n=8):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines[-n:]]

def build_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="top", size=5),
        Layout(name="middle", size=12),
        Layout(name="bottom")
    )
    layout["top"].split_row(
        Layout(name="status"),
        Layout(name="queue")
    )

    running = is_running()
    pid = get_pid()
    status_color = "green" if running else "red"
    status_text = Text()
    status_text.append("Status: ")
    status_text.append("RUNNING\n" if running else "STOPPED\n", style=status_color)
    status_text.append(f"PID: {pid if running else 'none'}")
    layout["status"].update(Panel(status_text, title="DAEMON", border_style=status_color))

    pending = get_pending()
    layout["queue"].update(Panel(
        "\n".join(pending) if pending else "[dim]none[/dim]",
        title="PENDING QUEUE",
        border_style="yellow"
    ))

    logs = get_last_logs()
    layout["middle"].update(Panel(
        "\n".join(logs) if logs else "[dim]no logs[/dim]",
        title="DAEMON LOG",
        border_style="blue"
    ))

    memory = recall(10)
    mem_table = Table(show_lines=True, expand=True)
    mem_table.add_column("Time", style="dim", width=20)
    mem_table.add_column("Goal", style="cyan")
    mem_table.add_column("Tasks", justify="right", width=6)
    for e in reversed(memory):
        mem_table.add_row(
            e["timestamp"][:19],
            e["goal"],
            str(len(e["tasks"]))
        )
    layout["bottom"].update(Panel(mem_table, title="GOAL HISTORY", border_style="magenta"))

    return layout

def main():
    with Live(build_layout(), refresh_per_second=0.5, screen=True) as live:
        while True:
            live.update(build_layout())
            time.sleep(2)

if __name__ == "__main__":
    main()
