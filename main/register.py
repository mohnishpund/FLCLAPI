from app import app
from flask import  request, json, jsonify, session
from database_conn import get_db_connection

import hashlib
from hashlib import md5
import re

@app.route('/register', methods=['POST'])
def register_user():
    try:
        conn = get_db_connection()

        cursor = conn.cursor()
        # here form request data in form

        forms = request.form
        email = forms['email']
        password = forms['password']

        # convert the password inot hashpassword
        hashpass1 = hashlib.md5(password.encode())
        hashpass2  = hashpass1.hexdigest()

        if request.method == 'POST':
            check_email = "SELECT * FROM USERS WHERE email = :email"
            e = (email, )
            cursor.execute(check_email, e)
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"error": "User with this email already exists."}), 400
            elif not email or not password:
                return jsonify({"error": "Email and password are required."}), 400
            elif not re.match(r'[A-Za-z0-9]+', email):
                return jsonify({"error": "Invalid email format."}), 400
            elif not re.match(r'[A-Za-z0-9]+', password):
                return jsonify({"error": "Password must be at least 8 characters long and contain both letters and numbers."}), 400
            else:
                d1 = "INSERT INTO USERS(email, password) VALUES(:email, :password)"
                d2 = (email, hashpass2)
                cursor.execute(d1, d2)
                conn.commit()
                cursor.close()

                msg = jsonify({
                    "success": "User registration is successful.",
                    "email": email,
                    "Converted secure Hash password": hashpass2}), 200
                return msg

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()