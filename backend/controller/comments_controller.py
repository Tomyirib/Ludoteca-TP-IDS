# Create Blueprint
from flask import Blueprint, jsonify, request

from repository.comments_repository import add_comment, get_rating_by_game_id, get_comments_by_game


# Define my blueprint
comentarios_bp = Blueprint("comments", __name__)


# get_comentarios_recientes devuelve los 10 comentarios mas recientes
@comentarios_bp.route("/recents")
def get_comentarios_recientes():
# def get_comentarios_recientes(cantidad):
    if not comentarios:
        return ("No hay comentarios recientes", 204)
    return jsonify(comentarios)


# get_comentarios_juego devuelve los comentarios mas recientes del juego pasado
@comentarios_bp.route("/<int:game_id>")
def get_comments_by_game_id(game_id):
    return get_comments_by_game(game_id)

# Subir comentario a base de datos
@comentarios_bp.route("/ingresar_comentario", methods=["POST"])
def add_comment():
    return add_comment(request.form.to_dict())

@comentarios_bp.route('/rating/<int:game_id>')
def get_rating_by_game_id(game_id):
    return get_rating_by_game_id(game_id)