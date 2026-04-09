import os
import importlib.util

PLUGIN_DIR = os.path.expanduser("~/zyp/plugins")


def load_plugins() -> dict:
    """
    Scans plugins/ directory and loads all valid plugin files.
    Returns dict of {tool_name: run_function}
    """
    plugins = {}
    if not os.path.exists(PLUGIN_DIR):
        return plugins

    for filename in os.listdir(PLUGIN_DIR):
        if not filename.endswith(".py") or filename.startswith("_"):
            continue

        path = os.path.join(PLUGIN_DIR, filename)
        try:
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            tool_name = getattr(module, "TOOL_NAME", None)
            run_fn = getattr(module, "run", None)

            if tool_name and callable(run_fn):
                plugins[tool_name] = {
                    "run": run_fn,
                    "description": getattr(module, "TOOL_DESCRIPTION", "no description"),
                    "args": getattr(module, "TOOL_ARGS", {})
                }
                print(f"[PLUGIN] Loaded: {tool_name} ({filename})")
            else:
                print(f"[PLUGIN] Skipped {filename} — missing TOOL_NAME or run()")

        except Exception as e:
            print(f"[PLUGIN] Failed to load {filename}: {e}")

    return plugins
