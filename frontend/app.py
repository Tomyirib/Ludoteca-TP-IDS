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

@app.route('/comunidad')
def comunidad():
    # dummy-data:
    comentario_1={"comentario_id":1,"usuario_id":41,"usuario_username":"The Viper","usuario_avatar":"pic10.jpg","juego_id":404,"juego_nombre":"Balatro","comentario_texto":"Este juego esta buenisimo, no veo la hora de jugarlo!","juego_imagen_cabecera":"pic01.jpg","comentario_timestamp":"2025-10-23 15:32"}
    comentario_2={"comentario_id":2,"usuario_id":17,"usuario_username":"BadBunny69","usuario_avatar":"pic11.jpg","juego_id":404,"juego_nombre":"CS:GO 2","juego_imagen_cabecera":"pic02.jpg","comentario_texto":"Ahhh! No me anda el mouse :'(","comentario_timestamp":"2025-11-12 11:24"}
    comentario_3={"comentario_id":3,"usuario_id":37,"usuario_username":"Tercero","usuario_avatar":"pic13.jpg","juego_id":242,"juego_nombre":"Age of Empires II","juego_imagen_cabecera":"pic03.jpg","comentario_texto":"Wololo!","comentario_timestamp":"2025-04-04 01:34"}
    comentarios_recientes=[comentario_1, comentario_2, comentario_3]
    # comentarios = obtener_comentarios_recientes()
    # masComentados = obtener_juegos_comentados()
    # if user.logeado == true:
        # comentarios_usuario = obtener_comentarios_usuario()
    return render_template('comunidad.html', brand=f"{BRAND} | Comunidad", comentarios_recientes=comentarios_recientes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)