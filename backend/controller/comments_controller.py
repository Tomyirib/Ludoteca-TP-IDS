from flask import Blueprint, jsonify, request

from repository.comments_repository import add_comment, get_rating_by_game_id, get_comments_by_game, get_recents, get_comments_by_user

comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/recents")
def get_recents_comments():
    return get_recents()

@comments_bp.route("/<int:game_id>")
def get_comments_by_game_id(game_id):
    return get_comments_by_game(game_id)

@comments_bp.route("/add", methods=["POST"])
def add():
    data = request.form.to_dict()
    usuario_id = int(data.get("usuario_id"))
    juego_id = int(data.get("juego_id"))
    comentario_texto = data.get("comentario_texto")
    rating = int(data.get("rating", 1))
    result = add_comment(usuario_id, juego_id, comentario_texto, rating)
    if result:
        return "Comentario ingresado correctamente", 201
    else:
        return "Problema al guardar", 500

@comments_bp.route('/rating/<int:game_id>')
def rating_by_game_id(game_id):
    return get_rating_by_game_id(game_id)


@comments_bp.route("/user/<int:usuario_id>")
def get_comments_users(usuario_id):
    return get_comments_by_user(usuario_id)