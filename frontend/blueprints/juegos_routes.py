from flask import Blueprint, render_template, session, request
import requests
from config import API_BASE
from utils.utils import get_game, get_user_name, obtener_comentarios_juego, obtener_valoracion_promedio
from config import BRAND

juegos_bp = Blueprint('juegos', __name__)

@juegos_bp.route('/juego/<int:game_id>', methods=['GET'])
def generic(game_id):
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    juego = get_game(game_id)
    if juego:
        comentarios_juego = obtener_comentarios_juego(game_id)
        valoracion_promedio = obtener_valoracion_promedio(game_id)
        return render_template('endpoints/generic.html', juego=juego, comentarios_recientes=comentarios_juego, rating_prom=valoracion_promedio, nombre=nombre)
    else:
        return "Juego no encontrado", 404
    

@juegos_bp.route('/catalogo')
def catalogo():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    page = int(request.args.get('page', 1))
    per_page = 12
    response = requests.get(f"http://backend:8080/games?page={page}&per_page={per_page}")
    data = response.json()
    juegos = data["games"]
    total = data["total"]
    return render_template('endpoints/catalogo.html', juegos=juegos, page=page, total=total, per_page=per_page, brand=BRAND, nombre=nombre)