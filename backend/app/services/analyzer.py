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
    cf_values = calculate_cf(metals) or {}
    dominant_source = get_dominant_metal(cf_values) or {}

    for index in indices:
        if index not in INDEX_FUNCTIONS:
            continue

        config = INDEX_FUNCTIONS[index]
        value = config["compute"](metals)
        classification = config["classify"](value)

        if config["type"] == "dict":
            # CF style
            entry = {
                "value": value,
                "classification": classification
            }
        else:
            # Scalar style
            entry = {
                "value": value,
                "classification": {
                    "level": classification.get("level") if classification else None,
                    "reason": classification.get("reason") if classification else None
                }
            }

        results[index] = entry

    # Add dominant pollution source info
    results["pollution_source"] = dominant_source

    # Build overall reasoning
    results["overall_reasoning"] = build_overall_reasoning(results)

    return results

def build_overall_reasoning(results):
    reasons = []

    for index, data in results.items():
        if index in ["pollution_source", "overall_reasoning"]:
            continue

        classification = data.get("classification")

        # Scalar indices
        if isinstance(classification, dict) and "reason" in classification:
            reasons.append(f"{index}: {classification['reason']}")
        # CF style (dict of metals)
        elif isinstance(classification, dict):
            for metal, meta in classification.items():
                reason = meta.get("reason")
                if reason:
                    reasons.append(f"{index} ({metal}): {reason}")

    return reasons