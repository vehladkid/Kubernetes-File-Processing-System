from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Directory where files are stored (mount point for PVC)
DATA_DIR = "/data"

# Simple HTML dashboard template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>File Dashboard</title>
  <style>
    body { font-family: Arial; background: #f5f5f5; text-align: center; padding: 20px; }
    table { margin: auto; border-collapse: collapse; width: 70%; }
    th, td { border: 1px solid #aaa; padding: 10px; }
    th { background: #333; color: #fff; }
    td { background: #fff; }
  </style>
</head>
<body>
  <h1>📁 File Dashboard</h1>
  {% if files %}
  <table>
    <tr><th>File Name</th><th>Download</th></tr>
    {% for file in files %}
      <tr>
        <td>{{ file }}</td>
        <td><a href="/download/{{ file }}">Download</a></td>
      </tr>
    {% endfor %}
  </table>
  {% else %}
  <p>No files found in /data</p>
  {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else []
    return render_template_string(TEMPLATE, files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
