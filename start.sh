#!/bin/bash

# Set environment variables
export DATABASE_URL="sqlite:///mydatabase.db"
export SECRET_KEY="your_secret_key"
export FLASK_APP="app:app"
export FLASK_ENV="production"

# Initialize the database
python -c "from app.database import init_db; init_db()"

# Start the application
gunicorn --bind 0.0.0.0:5050 --workers 4 --threads 2 app:app