from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from app import db  # Import db from app/__init__.py

class WaterQualityReport(db.Model):
    __tablename__ = "water_quality_reports"  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    location = db.Column(db.String(255), nullable=False)

    # Indices
    hpi_value = db.Column(db.Float, nullable=True)
    hei_value = db.Column(db.Float, nullable=True)
    cf_values = db.Column(db.JSON, nullable=True)
    pli_value = db.Column(db.Float, nullable=True)

    # Statuses
    hpi_status = db.Column(db.String(50), nullable=True)
    hei_status = db.Column(db.String(50), nullable=True)
    cf_status = db.Column(db.String(50), nullable=True)
    pli_status = db.Column(db.String(50), nullable=True)
    
    metals_data = db.Column(db.JSON, nullable=False)  # Store metal values as JSON

    def to_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created.isoformat(),
            "location": self.location,
            "hpi_value": self.hpi_value,
            "hei_value": self.hei_value,
            "cf_values": self.cf_values,
            "pli_value": self.pli_value,
            "hpi_status": self.hpi_status,
            "hei_status": self.hei_status,
            "cf_status": self.cf_status,
            "pli_status": self.pli_status,
            "metals_data": self.metals_data
        }