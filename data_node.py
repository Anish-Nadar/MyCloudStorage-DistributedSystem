import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # 1. IMPORT THE CORS LIBRARY
import argparse

app = Flask(__name__)
CORS(app)  # 2. ENABLE CORS FOR THE ENTIRE APP

STORAGE_DIR = None

@app.route('/store/<chunk_id>', methods=['POST'])
def store_chunk(chunk_id):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    chunk_path = os.path.join(STORAGE_DIR, chunk_id)
    with open(chunk_path, 'wb') as f:
        f.write(request.get_data())
    return jsonify({"message": f"Chunk {chunk_id} stored successfully."}), 201

@app.route('/retrieve/<chunk_id>', methods=['GET'])
def retrieve_chunk(chunk_id):
    chunk_path = os.path.join(STORAGE_DIR, chunk_id)
    if not os.path.exists(chunk_path):
        return jsonify({"error": "Chunk not found."}), 404
    return send_file(chunk_path)

@app.route('/delete/<chunk_id>', methods=['DELETE'])
def delete_chunk(chunk_id):
    chunk_path = os.path.join(STORAGE_DIR, chunk_id)
    if os.path.exists(chunk_path):
        os.remove(chunk_path)
        print(f"Deleted chunk {chunk_id}")
        return jsonify({"message": f"Chunk {chunk_id} deleted."}), 200
    else:
        return jsonify({"message": "Chunk not found, but proceeding."}), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a Data Node.")
    parser.add_argument('--port', type=int, required=True, help="Port to run on.")
    parser.add_argument('--dir', type=str, required=True, help="Directory to store chunks.")
    args = parser.parse_args()
    STORAGE_DIR = args.dir
    print(f"Data Node starting on port {args.port}, storing data in '{args.dir}'")
    app.run(host='0.0.0.0', port=args.port)

