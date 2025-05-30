from flask import Flask, request, jsonify
import requests
from steam_service import fetch_game_data

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
            password = request.form['password_login']
        elif 'email_signup' in request.form:
            email = request.form['email_signup']
            password = request.form['password_signup']
            first_name = request.form['first_name']
            last_name = request.form['last_name']

if __name__ == '__main__':
    app.run(debug=True, port=8080)