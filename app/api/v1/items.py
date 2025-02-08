from flask import Blueprint, request, jsonify
from app.database.models import Item
from app.database import db
from app.utils.errors import handle_exception
from prometheus_client import Counter, Histogram
import time  

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint']
)

items_blueprint = Blueprint("items", __name__)

# Track HTTP requests and latency
@items_blueprint.before_request
def before_request():
    request.start_time = time.time()  # Record the start time of the request

@items_blueprint.after_request
def after_request(response):
    latency = time.time() - request.start_time  # Calculate the latency
    REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

# Create an item
@items_blueprint.route("/items", methods=["POST"])
def create_item():
    try:
        data = request.get_json()
        if not data or "name" not in data:
            return jsonify({"error": "Name is required"}), 400

        item = Item(name=data["name"], description=data.get("description"))
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item created", "id": item.id}), 201
    except Exception as e:
        return handle_exception(e)

# Get all items
@items_blueprint.route("/items", methods=["GET"])
def get_all_items():
    try:
        items = Item.query.all()
        return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items]), 200
    except Exception as e:
        return handle_exception(e)

# Get a single item by ID
@items_blueprint.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        return jsonify({"id": item.id, "name": item.name, "description": item.description}), 200
    except Exception as e:
        return handle_exception(e)

# Update an item by ID
@items_blueprint.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    try:
        data = request.get_json()
        item = Item.query.get_or_404(item_id)

        if "name" in data:
            item.name = data["name"]
        if "description" in data:
            item.description = data["description"]

        db.session.commit()
        return jsonify({"message": "Item updated", "id": item.id}), 200
    except Exception as e:
        return handle_exception(e)

# Delete an item by ID
@items_blueprint.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted", "id": item.id}), 200
    except Exception as e:
        return handle_exception(e)