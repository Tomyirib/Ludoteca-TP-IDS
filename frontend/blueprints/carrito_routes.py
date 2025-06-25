from flask import Blueprint, render_template, session, request, redirect, flash, url_for
import requests
from config import BRAND
from utils.utils import get_game

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito')
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

    return render_template('carrito.carrito', brand=BRAND, juegos=juegos_carrito, total=round(total, 2))

@carrito_bp.route('/add', methods=['POST'])
def add():
    if 'email' not in session:
        flash('Debes iniciar sesión para agregar al carrito.', 'danger')
        return redirect(url_for('login'))
    game_id = request.form.get('game_id')
    carrito = session.get('carrito', [])
    carrito.append(game_id)
    session['carrito'] = carrito
    flash('Juego agregado al carrito.', 'success')
    return redirect(url_for('carrito.carrito'))

@carrito_bp.route('/eliminar', methods=['POST'])
def eliminar_del_carrito():
    game_id = request.form.get('game_id')
    if 'carrito' in session:
        session['carrito'] = [gid for gid in session['carrito'] if gid != game_id]
    flash('Juego eliminado del carrito.', 'info')
    return redirect(url_for('carrito.carrito'))

@carrito_bp.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    carrito = session.get('carrito', [])
    email = session.get('email')

    if not email or not carrito:
        flash('Debes iniciar sesión y tener juegos en el carrito.', 'danger')
        return redirect(url_for('carrito.carrito'))

    data = {
        'email': email,
        'game_ids': carrito
    }

    try:
        resp = requests.post('http://backend:8080/library/add', json=data)
        if resp.status_code == 200:
            session['carrito'] = []
            flash('Compra procesada. Juegos agregados a tu biblioteca.', 'success')
            return redirect(url_for('carrito.carrito'))
        else:
            error = resp.json().get('error', 'Error desconocido')
            flash(f'Error: {error}', 'danger')
            return redirect(url_for('carrito.carrito'))
    except Exception as e:
        flash(f'Error al conectar con backend: {e}', 'danger')
        return redirect(url_for('carrito.carrito'))