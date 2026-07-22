import requests

TOOL_NAME = "dictionary"
TOOL_DESCRIPTION = "looks up the definition of a word"
TOOL_ARGS = {"word": "str"}


def run(args: dict) -> dict:
    word = args.get("word", "").strip()

    if not word:
        return {"status": "error", "result": "no word provided"}

    try:
        r = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=10
        )
        if r.status_code != 200:
            return {"status": "error", "result": f"no definition found for '{word}'"}

        data = r.json()
        entry = data[0]
        meanings = entry.get("meanings", [])
        lines = [f"{word}:"]
        for m in meanings[:2]:
            pos = m.get("partOfSpeech", "")
            defs = m.get("definitions", [])
            if defs:
                lines.append(f"({pos}) {defs[0].get('definition', '')}")
        return {"status": "ok", "result": "\n".join(lines)}
    except Exception as e:
        return {"status": "error", "result": f"dictionary lookup failed: {e}"}
