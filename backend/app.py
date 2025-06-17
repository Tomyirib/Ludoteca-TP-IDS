from flask import Flask, request,render_template, jsonify, session, redirect, flash, url_for
import requests
from steam_service import fetch_game_data, get_all_games_data
from db_login import insert_user, login
from iniciar_db import connect_db as get_db_connection

app = Flask(__name__)

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
    if request.method == 'POST':
        if 'email_login' in request.form:
            email = request.form['email_login']
            contrasenia = request.form['password_login']

            if not all([email, contrasenia]):
                return jsonify({"error": "Faltan campos requeridos"}), 400
            
            result = login(email, contrasenia)

            if result:
                session['email'] = email
                session['first_name'] = result['first_name']
                session['last_name'] = result['last_name']
                return redirect(f'http://localhost:5000/?nombre={result["first_name"]}')
            else:
                flash("Email o contraseña incorrectos", "error")
                return redirect('http://127.0.0.1:5000/login') #corregir (otro puesto = eerorr)
        elif 'email_signup' in request.form:
            email = request.form['email_signup']
            contrasenia = request.form['password_signup']
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            if not all([email, contrasenia, first_name, last_name]):
                flash("Faltan campos requeridos", "error")
                return redirect('http://localhost:5000/login') #lo mismo, sale error con url_for
            
            result = insert_user(email, contrasenia, first_name, last_name)
            if result == "duplicado":
                flash("El usuario ya está registrado", "error")
                return redirect('http://localhost:5000/login')#lo mismo
            elif result is True:
                flash("Registro exitoso. Ahora podés iniciar sesión.", "success")
                return redirect('http://localhost:5000/login')#ño mismos
            else:
                flash("Error al registrar usuario", "error")
                return redirect('http://localhost:5000/login')#lo mismo
            
app.secret_key = "la_key_es_tp_intro_ludoteca"

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"mensaje": "Logout exitoso"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)