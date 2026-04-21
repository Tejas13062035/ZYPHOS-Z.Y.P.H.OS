import os
import requests
from tools.search import web_search
from core.llm import ask

REPORTS_DIR = os.path.expanduser("~/zyp/reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

NEXT_QUERY_PROMPT = """Research topic: {topic}
Notes so far: {summary}
Give ONE short follow-up search query (5 words max). Only the query, nothing else."""

REPORT_PROMPT = """Write a research report on: {topic}
Based on these notes:
{notes}
Write 3-5 paragraphs. Facts only. No fluff."""

def research(topic: str, depth: int = 3) -> str:
    print(f"\nRESEARCH: {topic}")
    notes = []
    query = topic

    for i in range(depth):
        print(f"[Round {i+1}] Query: {query}")
        results = web_search(query, max_results=3)
        if not results:
            break

        for r in results[:3]:
            if r.get("snippet"):
                note = f"Source: {r['title']}\n{r['snippet']}"
                notes.append(note)
                print(f"  Added: {r['title'][:60]}")

        if i < depth - 1 and notes:
            all_notes = "\n\n".join(notes[-4:])
            query = ask(
                f"Topic: {topic}\nNotes: {all_notes[:800]}",
                system=NEXT_QUERY_PROMPT.format(topic=topic, summary=all_notes[:500]),
                max_tokens=30
            ).strip().replace('"', '').replace("Search query:", "").strip()
            print(f"  Next query: {query}")

    if not notes:
        return "No research data found."

    print("\nGenerating report...")
    all_notes = "\n\n".join(notes)
    
    # use Groq for report — faster than local LLM for long generation
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": REPORT_PROMPT.format(topic=topic, notes=all_notes[:3000])},
                {"role": "user", "content": all_notes[:3000]}
            ],
            max_tokens=600
        )
        report = response.choices[0].message.content.strip()
    except Exception as e:
        report = f"Report generation failed: {e}"

    filename = topic.replace(" ", "_")[:50] + ".txt"
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, "w") as f:
        f.write(f"RESEARCH REPORT: {topic}\n")
        f.write("="*50 + "\n\n")
        f.write(report)
        f.write("\n\nSOURCES:\n")
        for n in notes:
            f.write(f"- {n.split(chr(10))[0]}\n")

    print(f"Report saved: {filepath}")
    return report
