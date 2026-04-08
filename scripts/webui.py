import os
import json
from flask import Flask, render_template_string, jsonify, request
from core.daemon import is_running, get_pid
from memory.store import recall

app = Flask(__name__)

GOAL_FILE = os.path.expanduser("~/zyp/state/pending_goals.txt")
LOG_FILE = os.path.expanduser("~/zyp/logs/daemon.log")

def get_pending():
    if not os.path.exists(GOAL_FILE):
        return []
    with open(GOAL_FILE, "r") as f:
        return [g.strip() for g in f.readlines() if g.strip()]

def get_last_logs(n=20):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines[-n:]]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Z.Y.P.H.O.S</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { background: #0a0a0a; color: #e0e0e0; font-family: monospace; padding: 20px; }
        h1 { color: #00ffcc; letter-spacing: 4px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
        .panel { background: #111; border: 1px solid #333; border-radius: 6px; padding: 16px; }
        .panel h3 { margin: 0 0 10px 0; font-size: 12px; letter-spacing: 2px; color: #888; }
        .running { color: #00ff88; }
        .stopped { color: #ff4444; }
        .log-line { font-size: 12px; color: #aaa; margin: 2px 0; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { text-align: left; color: #888; border-bottom: 1px solid #333; padding: 6px; }
        td { padding: 6px; border-bottom: 1px solid #1a1a1a; }
        td:first-child { color: #555; }
        td:nth-child(2) { color: #00ccff; }
        input { background: #1a1a1a; border: 1px solid #333; color: #fff; padding: 8px 12px; font-family: monospace; width: 70%; border-radius: 4px; }
        button { background: #00ffcc; color: #000; border: none; padding: 8px 16px; font-family: monospace; font-weight: bold; border-radius: 4px; cursor: pointer; margin-left: 8px; }
        .pid { color: #888; font-size: 13px; }
        .pending-item { color: #ffcc00; font-size: 13px; margin: 2px 0; }
    </style>
</head>
<body>
    <h1>Z.Y.P.H.O.S</h1>
    <div style="margin-bottom: 16px;">
        <input type="text" id="goalInput" placeholder="enter goal..." onkeydown="if(event.key==='Enter') sendGoal()">
        <button onclick="sendGoal()">SEND</button>
    </div>
    <div class="grid">
        <div class="panel">
            <h3>DAEMON</h3>
            <span class="{{ 'running' if running else 'stopped' }}">
                {{ 'RUNNING' if running else 'STOPPED' }}
            </span>
            <span class="pid"> — PID {{ pid if running else 'none' }}</span>
        </div>
        <div class="panel">
            <h3>PENDING QUEUE</h3>
            {% if pending %}
                {% for g in pending %}
                    <div class="pending-item">→ {{ g }}</div>
                {% endfor %}
            {% else %}
                <span style="color:#444">none</span>
            {% endif %}
        </div>
    </div>
    <div class="panel" style="margin-bottom: 16px;">
        <h3>DAEMON LOG</h3>
        {% for line in logs %}
            <div class="log-line">{{ line }}</div>
        {% endfor %}
    </div>
    <div class="panel">
        <h3>GOAL HISTORY</h3>
        <table>
            <tr><th>Time</th><th>Goal</th><th>Tasks</th></tr>
            {% for e in memory %}
            <tr>
                <td>{{ e.timestamp[:19] }}</td>
                <td>{{ e.goal }}</td>
                <td>{{ e.tasks|length }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    <script>
        function sendGoal() {
            const goal = document.getElementById('goalInput').value.trim();
            if (!goal) return;
            fetch('/send', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({goal})})
            .then(() => { document.getElementById('goalInput').value = ''; });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML,
        running=is_running(),
        pid=get_pid(),
        pending=get_pending(),
        logs=get_last_logs(),
        memory=list(reversed(recall(10)))
    )

@app.route("/send", methods=["POST"])
def send_goal():
    goal = request.json.get("goal", "").strip()
    if goal:
        with open(GOAL_FILE, "a") as f:
            f.write(goal + "\n")
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6789, debug=False)
