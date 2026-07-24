import requests
from core.llm import ask_cerebras

TOOL_NAME = "wisdom"
TOOL_DESCRIPTION = "shares a philosophical quote or tells a short philosophical/moral story"
TOOL_ARGS = {"mode": "str (quote|story)", "theme": "str (optional theme e.g. 'patience', 'change', 'courage')", "author": "str (optional philosopher name e.g. 'Marcus Aurelius', 'Nietzsche')"}


def _speak(text):
    try:
        requests.post("http://127.0.0.1:5000/speak", json={"text": text}, timeout=5)
    except Exception:
        pass


def _get_quote(theme="", author=""):
    if author:
        prompt = f"Give me one real, verifiable quote from {author}"
        if theme:
            prompt += f" about {theme}"
        prompt += ". Respond with ONLY the quote in quotes followed by an em dash and the author name. No other text."
    else:
        theme_part = f" about {theme}" if theme else " about life, wisdom, or the human condition"
        prompt = f"Give me one real, well-known philosophical quote{theme_part} from any famous philosopher. Respond with ONLY the quote in quotes followed by an em dash and the author name. No other text."

    result = ask_cerebras(prompt, system="You are a knowledgeable source of real philosophical quotes. Only cite quotes you are confident are accurate.", max_tokens=800)

    if result.startswith("LLM_ERROR"):
        return "The unexamined life is not worth living. — Socrates"

    return result.strip()


def _get_story(theme="", author=""):
    theme_prompt = f" about {theme}" if theme else ""
    style_prompt = f", written in the philosophical style and worldview of {author}" if author else ""
    prompt = f"Write a short philosophical parable or moral story{theme_prompt}{style_prompt}, in the style of Aesop or a Zen koan. Keep it under 150 words. End with a one-line moral."
    story = ask_cerebras(prompt, system="You are a wise storyteller who writes short, thought-provoking parables.", max_tokens=800)
    return story.strip()


def run(args: dict) -> dict:
    mode = args.get("mode", "quote").lower()
    theme = args.get("theme", "")
    author = args.get("author", "")

    try:
        if mode == "story":
            result = _get_story(theme, author)
        else:
            result = _get_quote(theme, author)

        _speak(result)
        return {"status": "ok", "result": result}
    except Exception as e:
        return {"status": "error", "result": f"wisdom failed: {e}"}
