from flask import Flask
import requests

app = Flask(__name__)

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game_id}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")


if __name__ == '__main__':
    app.run(debug=True, port=8080)