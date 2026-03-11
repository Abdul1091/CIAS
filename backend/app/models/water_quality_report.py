from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from app import db  # Import db from app/__init__.py

class WaterQualityReport(db.Model):
    __tablename__ = "water_quality_reports"  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    location = db.Column(db.String(255), nullable=False)
    hpi_value = db.Column(db.Float, nullable=False)
    hei_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    metals_data = db.Column(db.JSON, nullable=False)  # Store metal values as JSON

    def to_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "location": self.location,
            "hpi_value": self.hpi_value,
            "hei_value": self.hei_value,
            "status": self.status,
            "metals_data": self.metals_data
        }