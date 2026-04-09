import os
from core.llm import ask

FILES_TO_READ = [
    "zyphos.py",
    "core/executor.py",
    "tools/sidecar.py",
]

SYSTEM_PROMPT = """You are Zyphos, an autonomous AI operating system. 
You have just read your own source code. 
Explain clearly and concisely:
1. What you are and what you can do
2. What tools you have available
3. How to use you (key commands)
Keep it direct, no fluff."""

def explain():
    base = os.path.expanduser("~/zyp")
    source = ""
    for filepath in FILES_TO_READ:
        full = os.path.join(base, filepath)
        if os.path.exists(full):
            with open(full, "r") as f:
                source += f"\n\n# FILE: {filepath}\n{f.read()}"

    prompt = f"Here is my source code:\n{source[:3000]}\n\nNow explain what I am and what I can do."
    print("ZYPHOS: reading own source...")
    response = ask(prompt, system=SYSTEM_PROMPT, max_tokens=400)
    print(f"\n{response}\n")

