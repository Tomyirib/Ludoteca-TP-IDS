from flask import Flask, request,render_template, jsonify, session, redirect, flash, url_for
import requests
from steam_service import fetch_game_data, get_all_games_data
from db_login import insert_user, login
from iniciar_db import connect_db as get_db_connection

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

@app.route('/')

def back():
    return jsonify({"status": "OK", "message": "Backend API is running"}), 200

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM juegos WHERE id = %s", (game_id,))
    juego = cursor.fetchone()

    cursor.execute("""
        SELECT g.descripcion FROM generos g
        JOIN juego_genero jg ON g.id_genero = jg.id_genero
        WHERE jg.id_juego = %s
    """, (game_id,))
    generos = [row["descripcion"] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT c.descripcion FROM categorias c
        JOIN juego_categoria jc ON c.id = jc.categoria_id
        WHERE jc.juego_id = %s
    """, (game_id,))
    categorias = [row["descripcion"] for row in cursor.fetchall()]

    cursor.execute("SELECT url FROM screenshots WHERE juego_id = %s", (game_id,))
    screenshots = [row["url"] for row in cursor.fetchall()]

    cursor.execute("SELECT url FROM videos WHERE juego_id = %s", (game_id,))
    videos = [row["url"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

    juego["generos"] = generos
    juego["categorias"] = categorias
    juego["screenshots"] = screenshots
    juego["videos"] = videos

    return jsonify(juego)


@app.route('/games', methods=['GET'])
def get_games():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM juegos LIMIT %s OFFSET %s", (per_page, offset))
    juegos = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM juegos")
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return jsonify({
        "games": juegos,
        "total": total,
        "page": page,
        "per_page": per_page
    })

@app.route('/auth', methods=['POST'])
def api_login():
    if 'email_login' in request.form:
        email = request.form['email_login']
        password = request.form['password_login']

        if not all([email, password]):
            return jsonify({"error": "Faltan campos requeridos"}), 400
                
        result = login(email, password)

        if result:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Email o contraseña incorrectos"}), 401
        
    elif 'email_signup' in request.form:
        email = request.form['email_signup']
        password = request.form['password_signup']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if not all([email, password, first_name, last_name]):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        result = insert_user(email, password, first_name, last_name)
        if result == "duplicado":
            return jsonify({"error": "El usuario ya está registrado"}), 409
        elif result is True:
            return jsonify({"success": True}), 201
        else:
            return jsonify({"error": "Error al registrar usuario"}), 500
    else:
        return jsonify({"error": "Solicitud inválida"}), 400
            
@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name FROM usuario WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
@app.route('/eliminar', methods=['POST'])
def eliminar_del_carrito():
    game_id = request.form.get('game_id')
    if 'carrito' in session:
        session['carrito'] = [gid for gid in session['carrito'] if gid != game_id]
    flash('Juego eliminado del carrito.', 'info')
    return redirect(url_for('carrito'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)