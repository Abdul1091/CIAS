from flask import Blueprint, request, jsonify
from app.services.indices.hpi import calculate_hpi
from app.services.datasets.dataset_hpi_analysis import analyze_dataset
from app.models.water_quality_report import WaterQualityReport
from app.services.datasets.dataset_hei_analysis import analyze_dataset as analyze_hei_dataset
from app.services.indices.hei import calculate_hei
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
        hei_value=0.0,
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

    return df.to_json(orient="records")

@water_bp.route("/water/hpi", methods=["GET"])
def get_all_hpi_reports():
    """
    Retrieve all HPI reports
    ---
    tags:
      - Water Quality
    responses:
      200:
        description: List of HPI reports
    """
    reports = WaterQualityReport.query.all()
    return jsonify([report.to_dict() for report in reports])

@water_bp.route("/water/hpi/<int:report_id>", methods=["GET"])
def get_hpi_report(report_id):
    """
    Retrieve a single HPI report by ID
    ---
    tags:
      - Water Quality
    parameters:
      - name: report_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Single HPI report
      404:
        description: Report not found
    """
    report = db.session.get(WaterQualityReport, report_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report.to_dict())

@water_bp.route("/water/hei", methods=["POST"])
def compute_hei():
    """
    Compute Heavy Metal Evaluation Index (HEI)
    ---
    tags:
      - Water Quality
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            metals:
              type: array
              items:
                type: object
                properties:
                  metal:
                    type: string
                  measured:
                    type: number
    responses:
      200:
        description: HEI calculation result
    """
    data = request.json
    metals = data.get("metals")
    location = data.get("location")

    if not metals:
        return jsonify({"error": "Metals data required"}), 400

    hei = calculate_hei(metals)

    if hei is None:
        return jsonify({"error": "Unable to compute HEI"}), 400

    if hei < 10:
        status = "Low Pollution"
    elif hei <= 20:
        status = "Medium Pollution"
    else:
        status = "High Pollution"

    return jsonify({
        "HEI": hei,
        "status": status,
        "location": location
    })

@water_bp.route("/water/hei/dataset", methods=["POST"])
def compute_dataset_hei():
    """
    Compute HEI for a dataset
    """
    file = request.files["file"]
    df = analyze_hei_dataset(file)

    return df.to_json(orient="records")