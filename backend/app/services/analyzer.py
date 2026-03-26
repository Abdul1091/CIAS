from app.services.indices.hpi import calculate_hpi
from app.services.indices.hei import calculate_hei
from app.services.indices.pli import calculate_pli
from app.services.indices.cf import calculate_cf

from app.services.pollution_source import get_dominant_metal

from app.services.index_classifier import (
    classify_hpi,
    classify_hei,
    classify_pli,
    classify_cf
)


# Central registry of indices
INDEX_FUNCTIONS = {
    "HPI": {
        "compute": calculate_hpi,
        "classify": classify_hpi,
        "type": "scalar"
    },
    "HEI": {
        "compute": calculate_hei,
        "classify": classify_hei,
        "type": "scalar"
    },
    "PLI": {
        "compute": calculate_pli,
        "classify": classify_pli,
        "type": "scalar"
    },
    "CF": {
        "compute": calculate_cf,
        "classify": classify_cf,
        "type": "dict"
    },
}


def analyze_sample(metals, indices):
    """
    Compute selected water quality indices, provide classification,
    reasoning for each index, and dominant pollution source.
    """

    results = {}

    # Always compute CF to identify dominant pollution source
    cf_values = calculate_cf(metals)
    dominant_source = get_dominant_metal(cf_values)

    for index in indices:

        if index not in INDEX_FUNCTIONS:
            continue

        config = INDEX_FUNCTIONS[index]

        value = config["compute"](metals)

        # Build classification and reasoning
        classification = config["classify"](value)
        entry = {}

        if config["type"] == "dict":
            entry["values"] = value
            entry["classification"] = classification  # dict of metal -> category
        else:
            entry["value"] = value
            entry["classification"] = classification  # dict with level + reason

        # Add a human-readable reason for scalar indices
        if config["type"] != "dict" and isinstance(classification, dict):
            entry["reason"] = classification.get("reason")

        results[index] = entry

    # Add dominant pollution source info
    results["pollution_source"] = dominant_source

    # Build overall reasoning summary
    results["overall_reasoning"] = build_overall_reasoning(results)

    return results

def build_overall_reasoning(results):
    """
    Collects all reasoning from index classifications into a list of strings.
    """
    reasons = []

    for index, data in results.items():
        if index in ["pollution_source", "overall_reasoning"]:
            continue

        classification = data.get("classification")

        if isinstance(classification, dict):
            reason = classification.get("reason")
            if reason:
                reasons.append(f"{index}: {reason}")

    return reasons