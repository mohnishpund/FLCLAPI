from app import app
from flask import request, jsonify, session

from is_log_in import is_logged_in

#logout
@app.route("/logout", methods=['GET'])
@is_logged_in
def logout():
    session.clear()
    msg = jsonify({"success" : "You are now logged out"}), 200
    return msg