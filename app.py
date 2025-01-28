from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import logging
from prometheus_metrics import track_metrics
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

logging.basicConfig(level=logging.INFO)

def sanitize_input(data):
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")
    if 'name' not in data or 'description' not in data:
        raise ValueError("Missing required fields: 'name' and 'description'")
    if not isinstance(data['name'], str) or not isinstance(data['description'], str):
        raise ValueError("Fields 'name' and 'description' must be strings")
    return data

def get_db():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/items', methods=['POST'])
@track_metrics
def add_item():
    try:
        data = request.get_json()
        sanitized_data = sanitize_input(data)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (name, description) VALUES (?, ?)
        ''', (sanitized_data['name'], sanitized_data['description']))
        conn.commit()
        conn.close()
        
        app.logger.info(f"Item added: {sanitized_data}")
        return jsonify({"message": "Item added successfully"}), 201
    except ValueError as e:
        app.logger.error(f"Input validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/items/<int:item_id>', methods=['GET'])
@track_metrics
def get_item(item_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if item:
            return jsonify(dict(item)), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/items/<int:item_id>', methods=['DELETE'])
@track_metrics
def delete_item(item_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/items/<int:item_id>', methods=['PUT'])
@track_metrics
def update_item(item_id):
    try:
        data = request.get_json()
        sanitized_data = sanitize_input(data)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE items SET name = ?, description = ? WHERE id = ?
        ''', (sanitized_data['name'], sanitized_data['description'], item_id))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Item updated successfully"}), 200
    except ValueError as e:
        app.logger.error(f"Input validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    from database import init_db
    init_db()
    start_http_server(8000)  
    app.run(debug=True)