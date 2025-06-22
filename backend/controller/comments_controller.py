# Create Blueprint
from flask import Blueprint, jsonify, request

from repository.comments_repository import add_comment, get_rating_by_game_id, get_comments_by_game, get_recents

# Define my blueprint
comments_bp = Blueprint("comments", __name__)


# get_comentarios_recientes devuelve los 10 comentarios mas recientes
@comments_bp.route("/recents")
def get_recents_comments(request):
    return get_recents(request)

# get_comentarios_juego devuelve los comentarios mas recientes del juego pasado
@comments_bp.route("/<int:game_id>")
def get_comments_by_game_id(game_id):
    return get_comments_by_game(game_id)

# Subir comentario a base de datos
@comments_bp.route("/ingresar_comentario", methods=["POST"])
def add_comment():
    return add_comment(request.form.to_dict())

@comments_bp.route('/rating/<int:game_id>')
def get_rating_by_game_id(game_id):
    return get_rating_by_game_id(game_id)