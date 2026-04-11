import subprocess
import os

TOOL_NAME = "music"
TOOL_DESCRIPTION = "Play music by searching YouTube. Actions: play, stop, pause"
TOOL_ARGS = {"action": "play|stop|pause", "query": "song or artist name (for play)"}

PLAYER_PID_FILE = "/tmp/zyp_music.pid"

def run(args: dict) -> dict:
    action = args.get("action", "").lower()
    query = args.get("query", "")

    if action == "play":
        if not query:
            return {"error": "query required for play"}
        try:
            # stop any existing playback
            stop_music()
            # get audio URL via yt-dlp
            result = subprocess.run(
                ["yt-dlp", "-f", "bestaudio", "--get-url", f"ytsearch1:{query}"],
                capture_output=True, text=True, timeout=30
            )
            url = result.stdout.strip()
            if not url:
                return {"error": "no audio found"}
            # play with mpv in background
            proc = subprocess.Popen(
                ["mpv", "--no-video", "--really-quiet", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            with open(PLAYER_PID_FILE, "w") as f:
                f.write(str(proc.pid))
            return {"status": "playing", "query": query}
        except Exception as e:
            return {"error": str(e)}

    elif action == "stop":
        return stop_music()

    elif action == "pause":
        return {"status": "pause not supported in background mode — use stop"}

    else:
        return {"error": f"unknown action: {action}"}

def stop_music() -> dict:
    if not os.path.exists(PLAYER_PID_FILE):
        return {"status": "nothing playing"}
    try:
        with open(PLAYER_PID_FILE) as f:
            pid = int(f.read().strip())
        subprocess.run(["kill", str(pid)])
        os.remove(PLAYER_PID_FILE)
        return {"status": "stopped"}
    except Exception as e:
        return {"error": str(e)}
