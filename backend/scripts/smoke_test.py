import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


def load_env():
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(repo_root / ".env")
    load_dotenv(Path.cwd() / ".env")


def main() -> int:
    load_env()

    url = os.getenv("SMOKE_TEST_URL", "http://localhost:8000/plan")
    payload = {
        "origin": "San Francisco, CA",
        "destination": "Tokyo, Japan",
        "dates": "2026-03-10 to 2026-03-14",
        "travelers": 2,
        "budget_tier": "medium",
        "travel_style": "Culture",
        "interests": ["Food & Dining", "Art & Museums"],
    }

    try:
        resp = requests.post(url, json=payload, timeout=180)
    except Exception as exc:
        print(f"Smoke test failed: could not reach {url}. Error: {exc}")
        return 1

    print(f"status={resp.status_code}")
    if resp.status_code != 200:
        print(resp.text)
        return 1

    data = resp.json()
    status = data.get("status")
    print(f"plan_status={status}")

    plan = data.get("plan", {})
    hotels = plan.get("hotels_shortlist") or []
    first_hotel = (hotels[0].get("name") if hotels else "") or ""
    itinerary = plan.get("itinerary") or []
    first_activity = ""
    if itinerary and itinerary[0].get("morning_activities"):
        first_activity = itinerary[0]["morning_activities"][0].get("name", "")

    if "Mock Hotel" in first_hotel or "Morning exploration of" in first_activity:
        print("warning=mock_plan_detected")
        print("detail=LLM credentials likely not loaded; verify GEMINI_API_KEY and .env loading.")
        return 1

    print("result=ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
