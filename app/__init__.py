from flask import Flask
from app.config import Config
from app.database import init_db
from app.api.v1.items import items_blueprint
from app.utils.logging import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize logging
    setup_logging()

    # Initialize database
    init_db(app)

    # Register API blueprints
    app.register_blueprint(items_blueprint, url_prefix="/api/v1")

    return app