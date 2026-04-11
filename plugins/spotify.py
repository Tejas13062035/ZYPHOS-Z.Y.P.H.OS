import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/zyp/.env"))

TOOL_NAME = "spotify"
TOOL_DESCRIPTION = "Control Spotify: play, pause, next, previous, search and play a song or artist"
TOOL_ARGS = {"action": "play|pause|next|prev|search", "query": "song or artist name (for search)"}

SCOPE = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

def get_sp():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPE,
        cache_path=os.path.expanduser("~/zyp/state/.spotify_cache")
    ))

def run(args: dict) -> dict:
    action = args.get("action", "").lower()
    query = args.get("query", "")

    try:
        sp = get_sp()

        if action == "play":
            sp.start_playback()
            return {"status": "playing"}

        elif action == "pause":
            sp.pause_playback()
            return {"status": "paused"}

        elif action == "next":
            sp.next_track()
            return {"status": "skipped to next"}

        elif action == "prev":
            sp.previous_track()
            return {"status": "went to previous"}

        elif action == "search":
            if not query:
                return {"error": "query required for search"}
            results = sp.search(q=query, limit=1, type="track")
            tracks = results["tracks"]["items"]
            if not tracks:
                return {"error": f"no results for: {query}"}
            uri = tracks[0]["uri"]
            name = tracks[0]["name"]
            artist = tracks[0]["artists"][0]["name"]
            sp.start_playback(uris=[uri])
            return {"status": "playing", "track": name, "artist": artist}

        else:
            return {"error": f"unknown action: {action}"}

    except Exception as e:
        return {"error": str(e)}
