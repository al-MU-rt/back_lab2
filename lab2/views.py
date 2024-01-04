from lab2 import app
from flask import Flask, request, jsonify
from faker import Faker
from datetime import datetime
from lab2.models import User, Category, Record
import uuid

fake_users = {}
fake_categories = {}
fake_records = {}

@app.route("/")
def welcome_user():
    return f"<p>Welcome, user!</p><a href='/healthcheck'>Check Health</a>"

health_status = True
@app.route("/healthcheck")
def health_check():
    if health_status:
        response = jsonify(date=datetime.now(), status="OK")
        response.status_code = 200
    else:
        response = jsonify(date=datetime.now(), status="FAIL")
        response.status_code = 500
    return response

@app.route('/user/<user_id>', methods=['GET'])
def retrieve_user(user_id):
    user = fake_users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/user/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    user = fake_users.pop(user_id, None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/user', methods=['POST'])
def create_fake_user():
    user_data = request.get_json()

    # Check for required fields
    if "username" not in user_data:
        return jsonify({"error": "Username is required"}), 400

    # Generate a random identifier
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    fake_users[user_id] = user
    return jsonify(user)

@app.route('/users', methods=['GET'])
def retrieve_all_users():
    return jsonify(list(fake_users.values()))

@app.route('/category', methods=['GET'])
def retrieve_all_categories():
    return jsonify(list(fake_categories.values()))

@app.route('/category', methods=['POST'])
def create_fake_category():
    category_data = request.get_json()
    if "name" not in category_data:
        return jsonify({"error": "Name is required"}), 400
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data}
    fake_categories[category_id] = category
    return jsonify(category)

@app.route('/category', methods=['DELETE'])
def remove_category():
    category_id = request.args.get('id')

    if category_id:
        category = fake_categories.pop(category_id, None)
        if not category:
            return jsonify({"error": f"Category with id {category_id} not found"}), 404
        return jsonify(category)
    else:
        fake_categories.clear()
        return jsonify({"message": "All categories deleted"})

@app.route('/record/<record_id>', methods=['GET'])
def retrieve_record(record_id):
    record = fake_records.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record)

@app.route('/record/<record_id>', methods=['DELETE'])
def remove_record(record_id):
    record = fake_records.pop(record_id, None)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record)

@app.route('/record', methods=['POST'])
def create_fake_record():
    record_data = request.get_json()

    user_id = record_data.get('user_id')
    category_id = record_data.get('category_id')

    if not user_id or not category_id:
        return jsonify({"error": "Both user_id and category_id are required"}), 400

    if user_id not in fake_users:
        return jsonify({"error": f"User with id {user_id} not found"}), 404

    if category_id not in fake_categories:
        return jsonify({"error": f"Category with id {category_id} not found"}), 404

    record_id = uuid.uuid4().hex
    record = {"id": record_id, **record_data}
    fake_records[record_id] = record
    return jsonify(record)

@app.route('/record', methods=['GET'])
def retrieve_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({"error": "Specify user_id or category_id"}), 400

    filtered_records = [
        r for r in fake_records.values() if (not user_id or r['user_id'] == user_id) or (not category_id or r['category_id'] == category_id)
    ]
    return jsonify(filtered_records)