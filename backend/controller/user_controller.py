from flask import Blueprint, jsonify, request

user_bp = Blueprint("user", __name__)

@user_bp.route('/user/<email>', methods=['GET'])
def get_user(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name FROM usuario WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404