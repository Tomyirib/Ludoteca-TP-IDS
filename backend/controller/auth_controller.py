from flask import Blueprint, jsonify, request
from service.auth_service import register

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.form['email_signup']
    password = request.form['password_signup']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    if not all([email, password, first_name, last_name]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    result = register(email, password, first_name, last_name)
    if result == "duplicado":
        return jsonify({"error": "El usuario ya está registrado"}), 409
    elif result is True:
        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201
    else:
        return jsonify({"error": "No se pudo registrar el usuario"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email_login']
    password = request.form['password_login']

    if not all([email, password]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    result = login(email, password)

    if result:
        return jsonify({"mensaje": "Login exitoso"}), 200
    else:
        return jsonify({"error": "Email o contraseña incorrectos"}), 401