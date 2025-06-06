from flask import Flask, render_template, request
import requests

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'

@app.route('/')
def index():

    game_ids = [440, 570, 730, 578080, 271590, 292030, 359550, 252490, 381210, 105600, 275850, 346110]
    juegos = []
    for game_id in game_ids:
        juego = get_game(game_id)
        if juego:
            juegos.append(juego)

    return render_template('index.html', brand=BRAND, juegos=juegos)

@app.route('/juego/<int:game_id>', methods=['GET'])
def generic(game_id):
    juego = get_game(game_id)
    if juego:
        return render_template('generic.html', juego=juego, brand=BRAND)
    else:
        return print("Juego no encontrado"), 404

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', brand=BRAND)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html', brand=BRAND)

@app.route('/catalogo')
def catalogo():
    page = int(request.args.get('page', 1))
    per_page = 12
    response = requests.get(f"http://localhost:8080/games?page={page}&per_page={per_page}")
    data = response.json()
    juegos = data["games"]
    total = data["total"]
    return render_template('catalogo.html', juegos=juegos, page=page, total=total, per_page=per_page, brand=BRAND)

def get_game(game_id):
    response = requests.get(f"http://localhost:8080/games/{game_id}")

    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5001)