from flask import Blueprint, jsonify, request
from service.game_service import get_game_by_id, search_games

games_bp = Blueprint("games", __name__)

@games_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    result = get_game_by_id(game_id)

    if not result:
        return jsonify({"error": "Juego no encontrado"}), 404

    return jsonify(result)

@games_bp.route('/', methods=['GET'])
def get_games():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    
    games, total = search_games(page, per_page)
    
    return jsonify({
        "games": games,
        "total": total,
        "page": page,
        "per_page": per_page
    })