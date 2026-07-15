import requests
import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/zyp/.env"))

TOOL_NAME = "countries"
TOOL_DESCRIPTION = "Get info about any country - population, currency, capital, region"
TOOL_ARGS = {"country": "str: country name"}

def run(args=None):
    country = args.get("country", "India") if args else "India"
    api_key = os.getenv("RESTCOUNTRIES_API_KEY", "")

    # Try REST Countries v5 first
    if api_key:
        try:
            r = requests.get(
                f"https://api.restcountries.com/countries/v5?q={country}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            data = r.json()
            if data.get("success") and data.get("data"):
                d = data["data"][0]
                currencies = list(d.get("currencies", {}).values())
                currency = currencies[0]["name"] if currencies else "unknown"
                result = (
                    f"{d['name']['common']} — "
                    f"Capital: {list(d.get('capital', ['unknown']))[0]}, "
                    f"Population: {d.get('population', 0):,}, "
                    f"Currency: {currency}, "
                    f"Region: {d.get('region', 'unknown')}"
                )
                return {"status": "ok", "result": result, "source": "restcountries"}
        except Exception:
            pass  # fall through to Wikipedia

    # Fallback: Wikipedia
    try:
        r = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{country}",
            headers={"User-Agent": "Zyphos/1.0"},
            timeout=10
        )
        data = r.json()
        result = data.get("extract", "No info found")[:400]
        return {"status": "ok", "result": result, "source": "wikipedia"}
    except Exception as e:
        return {"error": str(e)}
