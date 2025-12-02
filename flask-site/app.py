from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
DB_PATH = os.path.join(UPLOAD_FOLDER, 'file_metadata.db')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- File type mapping ---
TYPE_FOLDERS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'docs': ['.pdf', '.txt', '.doc', '.docx', '.csv'],
}

def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for cat, exts in TYPE_FOLDERS.items():
        if ext in exts:
            return cat
    return 'others'

# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT,
            size INTEGER,
            type TEXT,
            upload_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Upload route ---
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            category = get_category(file.filename)
            folder = os.path.join(UPLOAD_FOLDER, category)
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, file.filename)
            file.save(filepath)

            # Save metadata to DB
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('INSERT INTO files (name, path, size, type, upload_date) VALUES (?, ?, ?, ?, ?)',
                      (file.filename, filepath, os.path.getsize(filepath), category, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()

            return redirect(url_for('upload_file'))

    # Get file list from DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, type FROM files')
    files = c.fetchall()
    conn.close()

    return render_template('index.html', files=files)

# --- Serve uploaded files ---
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    category = get_category(filename)
    return send_from_directory(os.path.join(UPLOAD_FOLDER, category), filename)

# --- Delete route ---
@app.route('/delete/<int:file_id>')
def delete_file(file_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT path FROM files WHERE id=?', (file_id,))
    result = c.fetchone()
    if result:
        file_path = result[0]
        if os.path.exists(file_path):
            os.remove(file_path)
        c.execute('DELETE FROM files WHERE id=?', (file_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('upload_file'))

# --- Dashboard Route ---
@app.route('/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*), SUM(size) FROM files')
    total_files, total_size = c.fetchone()

    c.execute('SELECT type, COUNT(*) FROM files GROUP BY type')
    type_stats = c.fetchall()

    conn.close()
    total_size = total_size or 0
    return render_template('stats.html', total_files=total_files, total_size=round(total_size / 1024, 2), type_stats=type_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
