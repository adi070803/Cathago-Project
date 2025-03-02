from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SESSION_PERMANENT'] = True
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, role, credits) VALUES (?, ?, ?, ?)',
                       (username, hashed_password, role, 20))
        conn.commit()
        return jsonify({'message': 'User registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    finally:
        conn.close()

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return jsonify({'message': 'Login successful', 'username': username, 'credits': user['credits']})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logout successful'})

@app.route('/user/profile', methods=['GET'])
def get_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, role, credits FROM users WHERE username = ?', (session['user'],))
    user = cursor.fetchone()
    conn.close()
    return jsonify(dict(user))

@app.route('/scan/upload', methods=['POST'])
def upload_document():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    file = request.files.get('file')
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET credits = credits - 1 WHERE username = ? AND credits > 0', (session['user'],))
        conn.commit()
        conn.close()
        return jsonify({'message': 'File uploaded and scanned', 'filepath': filepath})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/credits/request', methods=['POST'])
def request_credits():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET credits = credits + 10 WHERE username = ?', (session['user'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Credit request approved'})

@app.route('/admin/analytics', methods=['GET'])
def get_analytics():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, credits FROM users')
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        credits INTEGER DEFAULT 20
                     )''')
    conn.commit()
    conn.close()
    app.run(debug=True)
