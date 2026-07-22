import requests

TOOL_NAME = "translate"
TOOL_DESCRIPTION = "translates text to another language"
TOOL_ARGS = {"text": "str", "target_lang": "str (e.g. 'es', 'fr', 'hi', 'de')"}


def run(args: dict) -> dict:
    text = args.get("text", "").strip()
    target_lang = args.get("target_lang", "en").strip()

    if not text:
        return {"status": "error", "result": "no text provided"}

    try:
        r = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": f"en|{target_lang}"},
            timeout=10
        )
        data = r.json()
        translated = data.get("responseData", {}).get("translatedText", "")
        if not translated:
            return {"status": "error", "result": "translation failed"}
        return {"status": "ok", "result": translated}
    except Exception as e:
        return {"status": "error", "result": f"translate failed: {e}"}
