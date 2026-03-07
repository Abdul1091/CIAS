from flask import Blueprint, request, jsonify
from app.services.indices.hpi import calculate_hpi
from app.services.datasets.dataset_hpi_analysis import analyze_dataset
from app.models.water_quality_report import WaterQualityReport
from app import db

water_bp = Blueprint("water", __name__)

@water_bp.route("/water/hpi", methods=["POST"])
def compute_hpi():
    """
    Compute Heavy Metal Pollution Index (HPI)
    ---
    tags:
      - Water Quality
    consumes:
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
              example: River Niger
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
                    example: 0.05
    responses:
      200:
        description: HPI calculation result
        schema:
          type: object
          properties:
            HPI:
              type: number
            status:
              type: string
            report_id:
              type: integer
    """
    data = request.json
    metals = data.get("metals")
    location = data.get("location")

    if not metals:
        return jsonify({"error": "Metals data required"}), 400

    hpi = calculate_hpi(metals)
    status = "Safe" if hpi < 100 else "Polluted"
    report = WaterQualityReport(
        location=location,
        hpi_value=hpi,
        status=status,
        metals_data=metals
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "HPI": hpi,
        "status": status,
        "report_id": report.id
    })

@water_bp.route("/water/hpi/dataset", methods=["POST"])
def compute_dataset_hpi():
    """
    Compute HPI for a dataset
    ---
    tags:
      - Water Quality
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Dataset HPI results
    """
    file = request.files["file"]
    df = analyze_dataset(file)

    return df.to_json()