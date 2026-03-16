from app.services.reference_loader import get_reference_data


def calculate_cf(metals_data):
    """
    Calculate Contamination Factor (CF) for each metal.
    Returns dictionary {metal: CF}.
    """
    reference = get_reference_data()
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