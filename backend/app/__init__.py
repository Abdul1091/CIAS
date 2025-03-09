from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate  import Migrate
from .config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)

    # Import models to ensure they are registered before calling db.create_all()
    from .models import WaterQualityReport
    from .routes import hpi_bp

    app.register_blueprint(hpi_bp, url_prefix='/api')

    return app
