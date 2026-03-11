import json
from pathlib import Path

REFERENCE_FILE = Path(__file__).resolve().parents[2] / "reference_data" / "water_standards.json"


def load_reference_data():
    with open(REFERENCE_FILE) as f:
        return json.load(f)


def calculate_cf(metals_data):
    """
    Calculate Contamination Factor (CF) for each metal.
    Returns dictionary {metal: CF}.
    """
    reference = load_reference_data()
    results = {}

    for metal in metals_data:
        name = metal["metal"]
        measured = metal["measured"]

        if name not in reference:
            continue

        background = reference[name].get("background")

        if not background or background == 0:
            continue

        cf = measured / background
        results[name] = round(cf, 3)

    return results if results else None