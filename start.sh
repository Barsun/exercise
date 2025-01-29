#!/bin/bash

export DATABASE_URL="sqlite:///mydatabase.db"
export SECRET_KEY="your_secret_key"
export FLASK_APP="app.py"
export FLASK_ENV="production"

python -c "from app.database import init_db; init_db()"

gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 app:app