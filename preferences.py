"""
User preferences store — tracks who has opted out of Friday nudges.
Uses a simple JSON file. No database needed.
"""
import json
import os
import logging

logger = logging.getLogger(__name__)
PREFS_FILE = os.path.join(os.path.dirname(__file__), "user_prefs.json")


def _load() -> dict:
    if not os.path.exists(PREFS_FILE):
        return {"opted_out": []}
    with open(PREFS_FILE, "r") as f:
        return json.load(f)


def _save(data: dict):
    with open(PREFS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def is_opted_out(user_id: str) -> bool:
    return user_id in _load().get("opted_out", [])


def opt_out(user_id: str):
    data = _load()
    if user_id not in data["opted_out"]:
        data["opted_out"].append(user_id)
        _save(data)


def opt_in(user_id: str):
    data = _load()
    data["opted_out"] = [u for u in data["opted_out"] if u != user_id]
    _save(data)
