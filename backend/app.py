from flask import Flask, request, jsonify
import requests
from steam_service import fetch_game_data
from db_login import insert_user, login

app = Flask(__name__)

@app.route('/')
def back():
    return jsonify({"status": "OK", "message": "Backend API is running"}), 200

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    return fetch_game_data(game_id)

@app.route('/auth', methods=['POST'])
def api_login():
    if request.method == 'POST':
        if 'email_login' in request.form:
            email = request.form['email_login']
            contrasenia = request.form['password_login']

            if not all([email, contrasenia]):
                return jsonify({"error": "Faltan campos requeridos"}), 400
            
            result = login(email, contrasenia)

            if result == True:
                return jsonify({"mensaje": "Login exitoso"}), 201
            else:
                return jsonify({"error": "No se pudo completar el login"}), 500
        

        elif 'email_signup' in request.form:
            email = request.form['email_signup']
            contrasenia = request.form['password_signup']
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            if not all([email, contrasenia, first_name, last_name]):
                return jsonify({'error': 'Faltan campos requeridos'}), 400
            
            result = insert_user(email, contrasenia, first_name, last_name)
            if result == "duplicado":
                return jsonify({"error": "El usuario ya está registrado"}), 409
            elif result is True:
                return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201
            else:
                return jsonify({'error': 'No se pudo registrar el usuario'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)