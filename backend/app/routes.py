from flask import request, jsonify, Blueprint
from .models import db, WaterQualityReport
from .hpi_calculator import calculate_hpi

hpi_bp = Blueprint('hpi_calculator', __name__)

@hpi_bp.route('/calculate_hpi', methods=['POST'])
def calculate_and_store_hpi():
    data = request.get_json()

    if not data or "metals" not in data or "location" not in data:
        return jsonify({"error": "Invalid request. Provide 'metals' data and 'location'."}), 400

    try:
        hpi_value = calculate_hpi(data["metals"])
        status = "Safe" if hpi_value < 100 else "Polluted"

        # Store in database
        report = WaterQualityReport(
            location=data["location"],
            hpi_value=hpi_value,
            status=status,
            metals_data=data["metals"]
        )
        db.session.add(report)
        db.session.commit()

        return jsonify({"HPI": hpi_value, "status": status, "report_id": report.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message

@hpi_bp.route('/get_reports', methods=['GET'])
def get_reports():
    reports = WaterQualityReport.query.order_by(WaterQualityReport.date_created.desc()).all()
    return jsonify([report.to_dict() for report in reports])