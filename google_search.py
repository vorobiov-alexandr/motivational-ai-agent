# === google_search.py ===
import os
import requests

GOOGLE_API_KEY = os.getenv("AIzaSyBDXkHm1CWKrniC3LDH_Qm57JQT4EIuxhc")
SEARCH_ENGINE_ID = os.getenv("5612c1387fb4945ff")


def google_search(query, num_results=3):
    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        return ["Google API ключ или ID поисковой системы не заданы."]

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        return [item["link"] for item in results.get("items", [])]
    except Exception as e:
        return [f"Ошибка при поиске: {e}"]
