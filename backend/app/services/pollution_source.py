def get_dominant_metal(cf_dict):
    """
    Identify the metal contributing most to pollution and provide a
    consistent reasoning based on contamination factor.
    """
    if not cf_dict:
        return None

    dominant = max(cf_dict, key=cf_dict.get)
    value = cf_dict[dominant]

    # Determine impact level
    if value < 1:
        level = "Low"
        reason = f"{dominant} has the highest contamination factor, but CF < 1 indicates no significant pollution."
    elif value < 3:
        level = "Moderate"
        reason = f"{dominant} has the highest contamination factor, indicating moderate pollution."
    elif value < 6:
        level = "Considerable"
        reason = f"{dominant} has the highest contamination factor, indicating considerable pollution."
    else:
        level = "Very High"
        reason = f"{dominant} has the highest contamination factor, making it a very high pollution contributor."

    return {
        "metal": dominant,
        "cf_value": value,
        "impact_level": level,
        "reason": reason
    }