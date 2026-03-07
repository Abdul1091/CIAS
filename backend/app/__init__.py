from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate  import Migrate
from flasgger import Swagger
from .config import Config


db = SQLAlchemy()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "CIAS API",
        "description": "Computational Index Analysis System for Environmental Quality",
        "version": "1.0.0"
    }
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)

    Swagger(app, template=swagger_template)

    @app.route("/")
    def home():
        return {"message": "CIAS API running"}

    # Import models to ensure they are registered before calling db.create_all()
    from app.models.water_quality_report import WaterQualityReport
    from app.routes.water_routes import water_bp

    app.register_blueprint(water_bp, url_prefix='/api')

    return app
