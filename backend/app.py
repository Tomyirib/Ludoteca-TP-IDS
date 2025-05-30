from flask import Flask
import requests
from steam_service import fetch_game_data

app = Flask(__name__)

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    return fetch_game_data(game_id)

if __name__ == '__main__':
    app.run(debug=True, port=8080)