from flask import Blueprint, render_template, session
import requests
from config import API_BASE
from utils.utils import get_game, get_user_name, obtener_comentarios_juego, obtener_valoracion_promedio

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
        return render_template('generic.html', juego=juego, comentarios_recientes=comentarios_juego, rating_prom=valoracion_promedio, nombre=nombre)
    else:
        return "Juego no encontrado", 404