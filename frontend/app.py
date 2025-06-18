from flask import Flask, render_template, request, session, redirect, flash, url_for
import requests

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'
API_BASE = "http://localhost:8080"
app.secret_key = 'SECRET_KEY'

@app.route('/')
def index():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    game_ids = [440, 570, 730, 578080, 271590, 292030, 359550, 252490, 381210, 105600, 275850, 346110]
    juegos = []
    for game_id in game_ids:
        juego = get_game(game_id)
        if juego:
            juegos.append(juego)
    return render_template('index.html', juegos=juegos, nombre=nombre)

@app.route('/juego/<int:game_id>', methods=['GET'])
def generic(game_id):
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    juego = get_game(game_id)
    if juego:
        comentarios_juego = obtener_comentarios_juego(game_id)
        return render_template('generic.html', juego=juego, comentarios_recientes=comentarios_juego, nombre=nombre)
    else:
        return print("Juego no encontrado"), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    if request.method == 'POST':
        data = {
            'email_login': request.form['email_login'],
            'password_login': request.form['password_login']
        }
        resp = requests.post('http://localhost:8080/auth', data=data)
        if resp.status_code == 200:
            session['email'] = request.form['email_login']
            user = get_user_info(session['email'])
            session['first_name'] = user['first_name']
            session['es_admin'] = user['es_admin']
            session['esta_logueado'] = True
            session['usuario_id'] = user['id_usuario']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            mensaje = resp.json().get('error', 'Usuario o contraseña incorrectos')
            flash(mensaje, 'danger')
            return render_template('login.html', brand=BRAND, nombre=nombre)
    return render_template('login.html', brand=BRAND, nombre=nombre)

@app.route('/register', methods=['GET', 'POST'])
def register():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    if request.method == 'POST':
        data = {
            'email_signup': request.form['email_signup'],
            'password_signup': request.form['password_signup'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name']
        }
        resp = requests.post('http://localhost:8080/auth', data=data)
        if resp.status_code == 201:
            flash('Registro exitoso. Ya podés iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            mensaje = resp.json().get('error', 'Error al registrar usuario. Por favor, intente nuevamente.')
            flash(mensaje, 'danger')
    return render_template('login.html', brand=BRAND, nombre=nombre)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    if 'email' not in session:
        flash('Debes iniciar sesión para ver tu biblioteca.', 'danger')
        return redirect(url_for('login'))
    carrito_ids = session.get('carrito', [])
    juegos_carrito = []
    total = 0.0

    for game_id in carrito_ids:
        game_info = get_game(game_id)
        if game_info:
            juegos_carrito.append(game_info)

            price_str = game_info.get("price", "")
            if price_str and "Gratis" not in price_str:

                import re
                num = re.sub(r'[^\d,\.]', '', price_str)
                num = num.replace(",", ".")
                try:
                    total += float(num)
                except:
                    pass

    return render_template('carrito.html', brand=BRAND, juegos=juegos_carrito, total=round(total, 2))

@app.route('/add', methods=['POST'])
def add():
    if 'email' not in session:
        flash('Debes iniciar sesión para agregar al carrito.', 'danger')
        return redirect(url_for('login'))
    game_id = request.form.get('game_id')
    carrito = session.get('carrito', [])
    carrito.append(game_id)
    session['carrito'] = carrito
    flash('Juego agregado al carrito.', 'success')
    return redirect(url_for('carrito'))

@app.route('/catalogo')
def catalogo():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    page = int(request.args.get('page', 1))
    per_page = 12
    response = requests.get(f"http://localhost:8080/games?page={page}&per_page={per_page}")
    data = response.json()
    juegos = data["games"]
    total = data["total"]
    return render_template('catalogo.html', juegos=juegos, page=page, total=total, per_page=per_page, brand=BRAND, nombre=nombre)

@app.route('/biblioteca')
def biblioteca():
    nombre = None
    if 'email' not in session:
        flash('Debes iniciar sesión para ver tu biblioteca.', 'danger')
        return redirect(url_for('login'))
    nombre = get_user_name(session['email'])
    email = session['email']

    resp = requests.get(f'http://localhost:8080/biblioteca/{email}')
    if resp.status_code != 200:
        flash("Error al obtener la biblioteca", "danger")
        juegos = []
    else:
        juegos = resp.json().get('juegos', [])

    return render_template('biblioteca.html', brand=BRAND, juegos=juegos,nombre=nombre)

@app.route('/eliminar', methods=['POST'])
def eliminar_del_carrito():
    game_id = request.form.get('game_id')
    if 'carrito' in session:
        session['carrito'] = [gid for gid in session['carrito'] if gid != game_id]
    flash('Juego eliminado del carrito.', 'info')
    return redirect(url_for('carrito'))


@app.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    carrito = session.get('carrito', [])
    email = session.get('email')

    if not email or not carrito:
        flash('Debes iniciar sesión y tener juegos en el carrito.', 'danger')
        return redirect(url_for('carrito'))

    data = {
        'email': email,
        'game_ids': carrito
    }

    try:
        resp = requests.post('http://localhost:8080/biblioteca/agregar', json=data)
        if resp.status_code == 200:
            session['carrito'] = []
            flash('Compra procesada. Juegos agregados a tu biblioteca.', 'success')
            return redirect(url_for('carrito'))
        else:
            error = resp.json().get('error', 'Error desconocido')
            flash(f'Error: {error}', 'danger')
            return redirect(url_for('carrito'))
    except Exception as e:
        flash(f'Error al conectar con backend: {e}', 'danger')
        return redirect(url_for('carrito'))

def get_game(game_id):
    response = requests.get(f"http://localhost:8080/games/{game_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None



def get_user_name(email):
    resp = requests.get(f'http://localhost:8080/user/{email}')
    if resp.status_code == 200:
        return resp.json().get('first_name')
    return None

def get_user_info(email):
    resp = requests.get(f'http://localhost:8080/user_info/{email}')
    if resp.status_code == 200:
        return resp.json()
    return None

def obtener_comentarios_recientes():
    response = requests.get(f"{API_BASE}/comentarios/recientes")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_comentarios_juego(juego_id):
    response = requests.get(f"{API_BASE}/comentarios/juegos/{juego_id}")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_comentarios_usuario(usuario_id):
    response = requests.get(f"{API_BASE}/comentarios/usuario/{usuario_id}")
    if response.status_code == 200:
        return response.json()
    return []

@app.route('/comunidad')
def comunidad():
    comentarios_recientes = obtener_comentarios_recientes()
    comentarios_usuario = []
    if 'usuario_id' in session:
        comentarios_usuario = obtener_comentarios_usuario(session['usuario_id'])
    return render_template('comunidad.html', brand=f"{BRAND} | Comunidad", comentarios_recientes=comentarios_recientes, comentarios_usuario=comentarios_usuario)

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