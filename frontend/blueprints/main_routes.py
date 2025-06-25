from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import requests
from config import BRAND, API_BASE
from utils.utils import get_user_name, get_game

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
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
    return redirect(url_for('main.index'), juegos=juegos, nombre=nombre)

@main_bp.route('/carrito')
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

    return render_template('main.carrito', brand=BRAND, juegos=juegos_carrito, total=round(total, 2))

@main_bp.route('/biblioteca')
def biblioteca():
    nombre = None
    if 'email' not in session:
        flash('Debes iniciar sesión para ver tu biblioteca.', 'danger')
        return redirect(url_for('login'))
    nombre = get_user_name(session['email'])
    email = session['email']

    resp = requests.get(f'http://backend:8080/library/{email}')
    if resp.status_code != 200:
        flash("Error al obtener la biblioteca", "danger")
        juegos = []
    else:
        juegos = resp.json().get('juegos', [])

    return render_template('main.biblioteca', brand=BRAND, juegos=juegos,nombre=nombre)