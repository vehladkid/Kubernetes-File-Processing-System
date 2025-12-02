from flask import Flask, request, render_template_string, send_from_directory
import os

UPLOAD_FOLDER = "/data/uploads"
PROCESSED_FOLDER = "/data/processed"

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kubernetes File Dashboard</title>
    <style>
        body { font-family: Arial; margin: 40px; background-color: #f8f9fa; }
        h1 { color: #007bff; }
        h2 { margin-top: 30px; }
        form { margin-bottom: 20px; }
        table { width: 50%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #007bff; color: white; }
        a { text-decoration: none; color: #007bff; }
    </style>
</head>
<body>
    <h1>📂 Kubernetes File Dashboard</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>

    <h2>Uploaded Files</h2>
    <table>
        <tr><th>Name</th><th>Link</th></tr>
        {% for f in uploads %}
        <tr><td>{{ f }}</td><td><a href="/uploads/{{ f }}" target="_blank">View</a></td></tr>
        {% endfor %}
    </table>

    <h2>Processed Files</h2>
    <table>
        <tr><th>Name</th><th>Link</th></tr>
        {% for f in processed %}
        <tr><td>{{ f }}</td><td><a href="/processed/{{ f }}" target="_blank">View</a></td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    uploads = os.listdir(UPLOAD_FOLDER)
    processed = os.listdir(PROCESSED_FOLDER)
    return render_template_string(HTML_TEMPLATE, uploads=uploads, processed=processed)

@app.route("/upload", methods=["POST"])
def upload_file():
    f = request.files["file"]
    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)
    return "✅ File uploaded successfully! <a href='/'>Go back</a>"

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/processed/<path:filename>")
def serve_processed(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
