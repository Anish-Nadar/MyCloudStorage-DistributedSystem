# File: master_node.py

import json
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

# --- In-Memory Database ---
USERS = { "alice": "password123", "bob": "securepass456" }
user_file_to_chunks = { "alice": {}, "bob": {} }
chunk_to_datanodes = {}
DATA_NODES = ["http://localhost:5001"]
REPLICATION_FACTOR = 1

# --- Authentication & Endpoints ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', ' ').split(" ")[-1]
        if token not in USERS:
            return jsonify({"message": "Token is invalid or missing!"}), 401
        return f(current_user=token, *args, **kwargs)
    return decorated

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')
    if not username or not password: return jsonify({"message": "Username and password are required."}), 400
    if username in USERS: return jsonify({"message": "Username already exists."}), 409
    USERS[username] = password
    user_file_to_chunks[username] = {}
    return jsonify({"message": "Signup successful! Please log in."}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    username, password = auth.get('username'), auth.get('password')
    if username in USERS and USERS[username] == password:
        return jsonify({"token": username})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    data = request.get_json()
    filename, num_chunks = data['filename'], data['num_chunks']
    chunk_ids = [f"{current_user}_{filename}_chunk_{i}" for i in range(num_chunks)]
    user_file_to_chunks[current_user][filename] = chunk_ids
    upload_plan = []
    for chunk_id in chunk_ids:
        nodes = random.sample(DATA_NODES, k=min(REPLICATION_FACTOR, len(DATA_NODES)))
        chunk_to_datanodes[chunk_id] = nodes
        upload_plan.append({"chunk_id": chunk_id, "store_at": nodes})
    return jsonify(upload_plan)

@app.route('/download/<filename>', methods=['GET'])
@token_required
def download_file(current_user, filename):
    user_files = user_file_to_chunks.get(current_user, {})
    if filename not in user_files: return jsonify({"error": "File not found."}), 404
    chunk_ids = user_files[filename]
    plan = [{"chunk_id": cid, "retrieve_from": chunk_to_datanodes.get(cid)} for cid in chunk_ids]
    return jsonify(plan)

@app.route('/files', methods=['GET'])
@token_required
def list_files(current_user):
    return jsonify(list(user_file_to_chunks.get(current_user, {}).keys()))

# --- NEW FEATURE ---
@app.route('/delete/<filename>', methods=['DELETE'])
@token_required
def delete_file(current_user, filename):
    """Creates a plan for the client to delete file chunks and cleans up metadata."""
    user_files = user_file_to_chunks.get(current_user, {})
    if filename not in user_files:
        return jsonify({"error": "File not found."}), 404

    chunk_ids_to_delete = user_files[filename]
    delete_plan = []
    for chunk_id in chunk_ids_to_delete:
        locations = chunk_to_datanodes.get(chunk_id)
        if locations:
            delete_plan.append({"chunk_id": chunk_id, "delete_from": locations})
            # Clean up master's metadata for this chunk
            del chunk_to_datanodes[chunk_id]

    # Clean up master's metadata for this file
    del user_file_to_chunks[current_user][filename]
    
    print(f"Prepared delete plan for '{filename}' for user '{current_user}'")
    return jsonify(delete_plan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)