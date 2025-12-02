from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)

@app.route("/")
def index():
    files = []
    for f in sorted(os.listdir(DATA_DIR)):
        path = os.path.join(DATA_DIR, f)
        stat = os.stat(path)
        files.append({"name": f, "size": stat.st_size, "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat()})
    return jsonify({"files": files})

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "no file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "empty filename"}), 400
    safe_name = file.filename
    dest = os.path.join(DATA_DIR, safe_name)
    file.save(dest)
    return jsonify({"ok": True, "path": dest})

@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
