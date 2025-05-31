from flask import Flask, render_template, request
import requests

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'

@app.route('/')
def index():
    get_game()
    juegos = get_game()
    return render_template('index.html', brand=BRAND, juegos=juegos)

@app.route('/generic')
def generic():
    return render_template('generic.html', brand=BRAND)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', brand=BRAND)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html', brand=BRAND)


def get_game():
    GAME_IDS = [10, 570, 730, 346110, 70]  # tus IDs de prueba
    juegos = []

    for app_id in GAME_IDS:
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(url)
        if response.status_code != 200:
            continue
        data = response.json()
        if not data.get(str(app_id), {}).get("success"):
            continue
        game_data = data.get(str(app_id))["data"]
        juego = {
            "name": game_data.get("name"),
            "image": game_data.get("header_image")
        }
        juegos.append(juego)

    return juegos
    #response = requests.get("http://localhost:8080/games/440")

    #if response.status_code == 200:
    #    print(response.json())
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)