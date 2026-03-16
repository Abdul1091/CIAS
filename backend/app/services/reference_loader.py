import json
from pathlib import Path

REFERENCE_FILE = Path(__file__).resolve().parents[1] / "reference_data" / "water_standards.json"

_reference_cache = None


def get_reference_data():
    global _reference_cache

    if _reference_cache is None:
        with open(REFERENCE_FILE) as f:
            _reference_cache = json.load(f)

    return _reference_cache