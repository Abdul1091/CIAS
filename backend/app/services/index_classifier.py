def classify_hpi(hpi):
    """
    HPI interpretation.
    """
    if hpi is None:
        return None

    if hpi < 50:
        return {
            "level": "Low pollution",
            "reason": "HPI is below 50 indicating minimal heavy metal contamination"
        }
    elif hpi < 100:
        return {
            "level": "Moderate pollution",
            "reason": "HPI is between 50 and 100 indicating moderate contamination"
        }
    else:
        return {
            "level": "High pollution",
            "reason": "HPI exceeds 100 indicating significant heavy metal pollution"
        }


def classify_hei(hei):
    """
    HEI Interpretation.
    """
    if hei is None:
        return None

    if hei < 10:
        return {
            "level": "Low pollution",
            "reason": "HEI below 10 indicates low heavy metal exposure"
        }
    elif hei < 20:
        return {
            "level": "Moderate pollution",
            "reason": "HEI between 10–20 indicates moderate exposure risk"
        }
    else:
        return {
            "level": "High pollution",
            "reason": "HEI above 20 indicates high exposure risk"
        }


def classify_pli(pli):
    """
    PLI Interpretation.
    """
    if pli is None:
        return None

    if pli < 1:
        return {
            "level": "No pollution",
            "reason": "PLI below 1 indicates no overall pollution"
        }
    elif pli <= 2:
        return {
            "level": "Moderate pollution",
            "reason": "PLI between 1–2 indicates moderate pollution load"
        }
    else:
        return {
            "level": "High pollution",
            "reason": "PLI above 2 indicates high pollution load"
        }

def classify_cf(cf_dict):
    """
    CF interpretation"""
    if not cf_dict:
        return None

    classifications = {}

    for metal, cf in cf_dict.items():

        if cf < 1:
            level = "Low contamination"
            reason = "CF < 1 indicates no significant contamination"
        elif cf < 3:
            level = "Moderate contamination"
            reason = "CF between 1–3 indicates moderate contamination"
        elif cf < 6:
            level = "Considerable contamination"
            reason = "CF between 3–6 indicates considerable contamination"
        else:
            level = "Very high contamination"
            reason = "CF > 6 indicates severe contamination"

        classifications[metal] = {
            "level": level,
            "reason": reason
        }

    return classifications