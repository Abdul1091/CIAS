from flask import Blueprint, request, jsonify
import json
from app import db
from app.models.water_quality_report import WaterQualityReport
from app.logger import logger
from app.services.analyzer import analyze_sample

from app.services.datasets.dataset_index_analysis import analyze_index_dataset


water_bp = Blueprint("water", __name__)

ALLOWED_INDICES = {"HPI", "HEI", "PLI", "CF"}

@water_bp.route("/water/indices", methods=["POST"])
def compute_indices():
    """
    ---
    summary: Compute one or multiple water pollution indices
    description: |
      Computes selected water quality indices (HPI, HEI, PLI, CF) from provided metal measurements.
      Returns index values, classifications, overall reasoning, and dominant pollution source.
    tags:
      - Water Quality
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            location:
              type: string
              example: Katsina River
            indices:
              type: array
              items:
                type: string
                enum: ["HPI", "HEI", "PLI", "CF"]
              example: ["HPI", "HEI", "PLI", "CF"]
            metals:
              type: array
              items:
                type: object
                properties:
                  metal:
                    type: string
                    example: Pb
                  measured:
                    type: number
                    example: 0.12
    responses:
      200:
        description: Computed water quality report
      400:
        description: Missing metals data
    """
    data = request.get_json()
    metals = data.get("metals")
    indices = data.get("indices", list(ALLOWED_INDICES))
    location = data.get("location", "Unknown")

    logger.info(f"compute_indices called with location={location}, indices={indices}, metals={metals}")

    # Validate metals
    if not metals or not isinstance(metals, list):
        return jsonify({"error": "Metals data must be a non-empty list"}), 400

    for m in metals:
        if "metal" not in m or "measured" not in m:
            return jsonify({"error": "Each metal must have 'metal' and 'measured' fields"}), 400
        if not isinstance(m["measured"], (int, float)) or m["measured"] < 0:
            return jsonify({"error": f"Invalid measured value for {m.get('metal')}"}), 400
        
    # Validate indices
    invalid_indices = [idx for idx in indices if idx not in ALLOWED_INDICES]
    if invalid_indices:
        return jsonify({
            "error": f"Invalid indices {invalid_indices}",
            "allowed_indices": list(ALLOWED_INDICES)
        }), 400

    # Compute indices
    try:
        results = analyze_sample(metals, indices)
    except Exception as e:
        return jsonify({"error": "Index computation failed", "details": str(e)}), 500

    report = WaterQualityReport(
        location=location,
        metals_data=metals,
        hpi_value=results.get("HPI", {}).get("value"),
        hpi_status=results.get("HPI", {}).get("classification") or {},
        hei_value=results.get("HEI", {}).get("value"),
        hei_status=results.get("HEI", {}).get("classification") or {},
        pli_value=results.get("PLI", {}).get("value"),
        pli_status=results.get("PLI", {}).get("classification") or {},
        cf_values=results.get("CF", {}).get("value") or {},
        cf_status=results.get("CF", {}).get("classification") or {},
        pollution_source=results.get("pollution_source") or {},
        overall_reasoning=results.get("overall_reasoning") or []
    )

    db.session.add(report)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error("Index computation failed", exc_info=True)
        return jsonify({"error": "Database commit failed", "details": str(e)}), 500

    return jsonify({
        "report_id": report.id,
        "location": report.location,
        "indices": {
            "HPI": {"value": report.hpi_value, "classification": report.hpi_status},
            "HEI": {"value": report.hei_value, "classification": report.hei_status},
            "PLI": {"value": report.pli_value, "classification": report.pli_status},
            "CF": {"value": report.cf_values, "classification": report.cf_status},
        },
        "pollution_source": report.pollution_source,
        "overall_reasoning": report.overall_reasoning
    })

@water_bp.route("/water/dataset/<index>", methods=["POST"])
def compute_dataset_index(index):
    """
    ---
    summary: Compute pollution index from dataset
    description: |
      Computes the specified water pollution index (HPI, HEI, PLI, CF) for each row
      in a CSV or Excel dataset. Returns index values, classifications, overall reasoning,
      and dominant pollution source per row.
    tags:
      - Water Quality
    parameters:
      - name: index
        in: path
        required: true
        type: string
        enum: ["HPI", "HEI", "PLI", "CF"]
      - name: file
        in: formData
        type: file
        required: true
        description: CSV or Excel file containing metal concentrations
    consumes:
      - multipart/form-data
    responses:
      200:
        description: Dataset analysis results
      400:
        description: Invalid index or missing file
    """
    file = request.files.get("file")
    index = index.upper()

    if index not in ALLOWED_INDICES:
        logger.warning(f"Invalid index '{index}' submitted")
        return jsonify({
            "error": f"Invalid index '{index}'",
            "allowed_indices": list(ALLOWED_INDICES)
        }), 400

    if not file:
        logger.warning("Dataset file missing in request")
        return jsonify({"error": "Dataset file required"}), 400

    # Determine file type
    filename = file.filename.lower()
    if filename.endswith(".csv"):
        file_type = "csv"
    elif filename.endswith((".xls", ".xlsx")):
        file_type = "excel"
    else:
        logger.warning(f"Unsupported file type uploaded: {filename}")
        return jsonify({"error": "Unsupported file type. Upload CSV or Excel file."}), 400

    logger.info(f"compute_dataset_index called for index={index}, file={filename}, type={file_type}")

    try:
        df = analyze_index_dataset(file, index)
    except Exception as e:
        logger.error(f"Dataset analysis failed for index={index}", exc_info=True)
        return jsonify({"error": "Dataset analysis failed", "details": str(e)}), 500

    # Convert to JSON
    results = json.loads(df.to_json(orient="records"))
    return jsonify({"index": index, "results": results})