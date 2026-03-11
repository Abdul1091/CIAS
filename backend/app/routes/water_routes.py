from flask import Blueprint, request, jsonify
from app.services.indices.hpi import calculate_hpi
from app.services.datasets.dataset_hpi_analysis import analyze_dataset
from app.models.water_quality_report import WaterQualityReport
from app.services.datasets.dataset_hei_analysis import analyze_dataset as analyze_hei_dataset
from app.services.indices.hei import calculate_hei
from app.services.indices.cf import calculate_cf
from app.services.datasets.dataset_cf_analysis import analyze_dataset as analyze_cf_dataset
from app.services.indices.pli import calculate_pli
from app.services.datasets.dataset_pli_analysis import analyze_dataset as analyze_pli_dataset
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
    hpi_status = "Safe" if hpi < 100 else "Polluted"
    report = WaterQualityReport(
        location=location,
        hpi_value=hpi,
        hei_value=0.0,
        hpi_status=hpi_status,
        metals_data=metals
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "HPI": hpi,
        "hpi_status": hpi_status,
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
    location = data.get("location", "Unknown") 

    if not metals:
        return jsonify({"error": "Metals data required"}), 400

    hei = calculate_hei(metals)

    if hei is None:
        return jsonify({"error": "Unable to compute HEI"}), 400

    if hei < 10:
        hei_status = "Low Pollution"
    elif hei <= 20:
        hei_status = "Medium Pollution"
    else:
        hei_status = "High Pollution"

    report = WaterQualityReport(
        location=location,
        hei_value=hei,
        hei_status=hei_status,
        metals_data=metals
        )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "HEI": hei,
        "hei_status": hei_status,
        "report_id": report.id
    })

@water_bp.route("/water/hei/dataset", methods=["POST"])
def compute_dataset_hei():
    """
    Compute Contamination Factor (CF) for a dataset (CSV)
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
        description: Dataset HEI results
    """
    file = request.files["file"]
    df = analyze_hei_dataset(file)

    return df.to_json(orient="records")

@water_bp.route("/water/cf", methods=["POST"])
def compute_cf():
    """
    Compute Contamination Factor (CF) for metals
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
                  measured:
                    type: number
    responses:
      200:
        description: CF calculation result
    """
    data = request.json
    metals = data.get("metals")
    location = data.get("location", "Unknown")

    if not metals:
        return jsonify({"error": "Metals data required"}), 400

    cf_values = calculate_cf(metals)
    if not cf_values:
        return jsonify({"error": "Unable to compute CF"}), 400

    # Optional CF status based on CF values (example logic)
    cf_status = "Low Pollution"
    if any(v > 3 for v in cf_values.values()):
        cf_status = "High Pollution"
    elif any(v > 1 for v in cf_values.values()):
        cf_status = "Medium Pollution"

    # Save report to DB
    report = WaterQualityReport(
        location=location,
        hpi_value=0.0,
        hei_value=0.0,
        cf_values=cf_values,
        metals_data=metals,
        cf_status=cf_status,
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "CF": cf_values,
        "cf_status": cf_status,
        "report_id": report.id
    })

@water_bp.route("/water/cf/dataset", methods=["POST"])
def compute_dataset_cf():
    """
    Compute Contamination Factor (CF) for a dataset (CSV)
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
        description: Dataset CF results
    """
    file = request.files["file"]
    df = analyze_cf_dataset(file)
    return df.to_json(orient="records")

@water_bp.route("/water/pli", methods=["POST"])
def compute_pli():
    """
    Compute Pollution Load Index (PLI)
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
            location:
              type: string
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
        description: PLI calculation result
        schema:
          type: object
          properties:
            PLI:
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

    pli = calculate_pli(metals)
    if pli is None:
        return jsonify({"error": "Unable to compute PLI"}), 400

    # Status based on threshold (commonly: PLI >1 polluted)
    pli_status = "Safe" if pli <= 1 else "Polluted"

    report = WaterQualityReport(
        location=location,
        pli_value=pli,
        pli_status=pli_status,
        metals_data=metals
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({
        "PLI": pli,
        "pli_status": pli_status,
        "report_id": report.id
    })

@water_bp.route("/water/pli/dataset", methods=["POST"])
def compute_dataset_pli():
    """
    Compute PLI for a dataset
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
        description: Dataset PLI results
    """
    file = request.files["file"]
    df = analyze_pli_dataset(file)

    return df.to_json(orient="records")