from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Create a connection and check if the table exists
        with db.engine.connect() as connection:
            inspector = inspect(connection)
            if not inspector.has_table("item"):
                db.create_all()