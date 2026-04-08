import requests

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "phi-3.5-mini-instruct"

def ask(prompt: str, system: str = "", max_tokens: int = 150) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        r = requests.post(LM_STUDIO_URL, json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.2
        }, timeout=120)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLM_ERROR: {e}"
