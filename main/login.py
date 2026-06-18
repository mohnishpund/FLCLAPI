from app import app
from flask import jsonify, request, session
from database_conn import get_db_connection
import hashlib


@app.route('/login', methods=['POST'])
def login_user():
    conn = None
    cursor = None

    try:
        if session.get('logged_in') is True:
            return jsonify({'error': 'User is already logged in.'}), 400

        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400

        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        query = "SELECT * FROM users WHERE email = :1 AND password = :2"
        cursor.execute(query, (email, hashed_password))
        account = cursor.fetchone()

        if account:
            session['logged_in'] = True
            session['email'] = email
            return jsonify({'success': 'Logged in successfully'}), 200

        return jsonify({'error': 'Incorrect email/password'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()