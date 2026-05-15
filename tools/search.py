import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger("ddgs").setLevel(logging.ERROR)
from ddgs import DDGS

def web_search(query: str, max_results: int = 5) -> list:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })
    return results

def search_summary(query: str, max_results: int = 3) -> str:
    results = web_search(query, max_results)
    if not results:
        return "No results found."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']}")
        lines.append(f"   {r['snippet']}")
        lines.append(f"   {r['url']}")
    return "\n".join(lines)
