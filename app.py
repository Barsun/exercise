from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def sanitize_input(data):
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")
    if 'name' not in data or 'description' not in data:
        raise ValueError("Missing required fields: 'name' and 'description'")
    if not isinstance(data['name'], str) or not isinstance(data['description'], str):
        raise ValueError("Fields 'name' and 'description' must be strings")
    return data

@app.route('/items', methods=['POST'])
def add_item():
    try:
        data = request.get_json()
        sanitized_data = sanitize_input(data)
        
        from database import insert_item
        insert_item(sanitized_data['name'], sanitized_data['description'])
        
        app.logger.info(f"Item added: {sanitized_data}")
        return jsonify({"message": "Item added successfully"}), 201
    except ValueError as e:
        app.logger.error(f"Input validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)