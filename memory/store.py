import json
import os
import numpy as np
from datetime import datetime

MEMORY_FILE = os.path.expanduser("~/zyp/state/memory.json")
INDEX_FILE = os.path.expanduser("~/zyp/state/memory.index")

_model = None
_index = None
_entries = []


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_index():
    global _index, _entries
    import faiss
    if _index is None:
        _entries = _load_entries()
        _index = faiss.IndexFlatL2(384)
        if _entries:
            model = _get_model()
            vectors = model.encode([e["goal"] for e in _entries]).astype("float32")
            _index.add(vectors)
    return _index


def _load_entries():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_entries(entries):
    with open(MEMORY_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def save(goal: str, tasks: list):
    global _index, _entries
    import faiss

    entry = {
        "goal": goal,
        "tasks": [t.get("description", "") for t in tasks],
        "timestamp": datetime.now().isoformat()
    }

    _entries = _load_entries()
    _entries.append(entry)
    _save_entries(_entries)

    # add to index
    model = _get_model()
    vector = model.encode([goal]).astype("float32")
    index = _get_index()
    index.add(vector)
    print(f"MEMORY: saved + indexed ({len(_entries)} total)")


def recall(query: str, top_k: int = 5) -> list:
    entries = _load_entries()
    if not entries:
        return []

    # if query is an int (legacy call), fall back to last N
    if isinstance(query, int):
        return entries[-query:]

    model = _get_model()
    index = _get_index()

    vector = model.encode([query]).astype("float32")
    k = min(top_k, len(entries))
    distances, indices = index.search(vector, k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(entries):
            results.append(entries[idx])
    return results
