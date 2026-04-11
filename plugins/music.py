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
            stop_music()
            # download audio to shared path
            out_path = "/mnt/c/zyphos_sidecar/music.mp3"
            win_path = r"C:\zyphos_sidecar\music.mp3"
            result = subprocess.run(
                ["yt-dlp", "-f", "bestaudio/best", 
                 "-o", "/mnt/c/zyphos_sidecar/music.%(ext)s",
                 "--no-playlist",
                 f"ytsearch1:{query}"],
                capture_output=True, text=True, timeout=120
            )
            # find the downloaded file
            import glob
            files = glob.glob("/mnt/c/zyphos_sidecar/music.*")
            if not files:
                return {"error": "download failed"}
            out_path = files[0]
            win_path = r"C:\zyphos_sidecar\\" + os.path.basename(out_path)
            import requests as req
            r = req.post("http://127.0.0.1:5000/play_audio", json={"path": win_path})
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
    try:
        import requests as req
        req.post("http://127.0.0.1:5000/stop_audio")
    except:
        pass
    return {"status": "stopped"}
