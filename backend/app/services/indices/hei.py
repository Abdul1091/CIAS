import json
from pathlib import Path

REFERENCE_FILE = Path(__file__).resolve().parents[2] / "reference_data" / "water_standards.json"


def load_reference_data():
    with open(REFERENCE_FILE) as f:
        return json.load(f)


def calculate_hei(metals_data):
    reference = load_reference_data()
    hei = 0

    for metal in metals_data:
        name = metal["metal"]
        measured = metal["measured"]

        if name not in reference:
            continue

        permissible = reference[name]["permissible"]

        if permissible == 0:
            continue

        hei += measured / permissible

    return round(hei, 3) if hei != 0 else None