from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'
API_BASE = "http://localhost:8080"

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
        comentarios_juego = obtener_comentarios_juego(game_id)
        return render_template('generic.html', juego=juego, brand=BRAND, comentarios_recientes=comentarios_juego)
    else:
        return print("Juego no encontrado"), 404

@app.route('/login')
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

def obtener_comentarios_recientes():
    response = requests.get(f"{API_BASE}/comentarios/recientes")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_comentarios_juego(juego_id):
    response = requests.get(f"{API_BASE}/comentarios/{juego_id}")
    if response.status_code == 200:
        return response.json()
    return []

@app.route('/comunidad')
def comunidad():
    comentarios_recientes = obtener_comentarios_recientes()
    # comentarios_usuario = obtener_comentarios_usuario()
    return render_template('comunidad.html', brand=f"{BRAND} | Comunidad", comentarios_recientes=comentarios_recientes)

@app.route('/post_comentario', methods=["POST"])
def post_comentario():
    comentario_data = request.form.to_dict()
    # Ver si session esta iniciada
    # Si no hay usuario en session flash error
    # Armar comentario con informacion de session
    comentario_data["usuario_id"] = "1"
    redirect_id = int(request.form["juego_id"])
    # Request al API
    response = requests.post(f"{API_BASE}/comentarios/ingresar_comentario", comentario_data)
    # Si error en API
    if response.status_code == 500:
        # Flash error
        return print("No se pudo ingresar comentario desde backend"), 500

    # si todo bien, redirijo a la misma pagina
    return redirect(url_for('generic', game_id=redirect_id))

if __name__ == '__main__':
    app.run(debug=True, port=5000)