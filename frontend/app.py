from flask import Flask, render_template, request, session, redirect, flash, url_for
import requests

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'
app.secret_key = 'SECRET_KEY'

@app.route('/')
def index():
    nombre = None
    if 'user_id' in session:
        nombre = get_user_name(session['user_id'])
    game_ids = [440, 570, 730, 578080, 271590, 292030, 359550, 252490, 381210, 105600, 275850, 346110]
    juegos = []
    for game_id in game_ids:
        juego = get_game(game_id)
        if juego:
            juegos.append(juego)
    return render_template('index.html', brand=BRAND, juegos=juegos, nombre=nombre)

# CAMBIAR/QUITAR ESTO 
@app.context_processor
def inject_user_name():
    nombre = None
    if 'user_id' in session:
        nombre = get_user_name(session['user_id'])
    return dict(nombre=nombre)

@app.route('/juego/<int:game_id>', methods=['GET'])
def generic(game_id):
    juego = get_game(game_id)
    if juego:
        return render_template('generic.html', juego=juego, brand=BRAND)
    else:
        return print("Juego no encontrado"), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'email_login': request.form['email_login'],
            'password_login': request.form['password_login']
        }
        resp = requests.post('http://localhost:8080/auth', data=data, allow_redirects=False)
        if resp.status_code == 302:
            user_id = resp.headers.get('X-User-Id')
            session['user_id'] = request.form['first_name']
            session['email'] = request.form['email_login']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html', brand=BRAND)
    return render_template('login.html', brand=BRAND)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'email_signup': request.form['email_signup'],
            'password_signup': request.form['password_signup'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name']
        }
        resp = requests.post('http://localhost:8080/auth', data=data, allow_redirects=False)
        if resp.status_code == 302:
            flash('Registro exitoso. Ya podés iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar usuario. Por favor, intente nuevamente.', 'danger')
    return render_template('login.html', brand=BRAND)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    return render_template('carrito.html', brand=BRAND)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
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
    
def get_user_name(user_id):
    resp = requests.get(f'http://localhost:8080/user/{user_id}')
    if resp.status_code == 200:
        return resp.json().get('first_name')
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)