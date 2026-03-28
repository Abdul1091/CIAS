from sqlalchemy import Column, JSON
from datetime import datetime, timezone

from app import db  # Import db from app/__init__.py

class WaterQualityReport(db.Model):
    __tablename__ = "water_quality_reports"  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_modified = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
        )
    location = db.Column(db.String(255), nullable=False)

    # Indices
    hpi_value = db.Column(db.Float, nullable=True)
    hei_value = db.Column(db.Float, nullable=True)
    cf_values = db.Column(db.JSON, nullable=True)
    pli_value = db.Column(db.Float, nullable=True)

    # Statuses
    hpi_status = db.Column(db.JSON, nullable=True)
    hei_status = db.Column(db.JSON, nullable=True)
    cf_status = db.Column(db.JSON, nullable=True)
    pli_status = db.Column(db.JSON, nullable=True)
    pollution_source = db.Column(db.JSON, nullable=True)
    overall_reasoning = db.Column(db.JSON, nullable=True)
    
    # Raw metal measurements
    metals_data = db.Column(db.JSON, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created.isoformat(),
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,
            "location": self.location,
            "hpi_value": self.hpi_value,
            "hei_value": self.hei_value,
            "cf_values": self.cf_values,
            "pli_value": self.pli_value,
            "hpi_status": self.hpi_status,
            "hei_status": self.hei_status,
            "cf_status": self.cf_status,
            "pli_status": self.pli_status,
            "metals_data": self.metals_data,
            "pollution_source": self.pollution_source,
            "overall_reasoning": self.overall_reasoning
        }