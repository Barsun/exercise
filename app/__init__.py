from flask import Flask
from app.config import Config
from app.database import init_db
from app.api.v1.items import items_blueprint
from app.utils.logging import setup_logging
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize logging
    setup_logging()

    # Initialize database
    init_db(app)

    # Register API blueprints
    app.register_blueprint(items_blueprint, url_prefix="/api/v1")

    # Swagger UI
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.json"
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "MyApp API"},
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app