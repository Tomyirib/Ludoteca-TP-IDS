from repository.library_repository import add_library as add
from repository.library_repository import get_library as get
from flask import jsonify

def add_library(request):
    email = request.get('email')
    game_ids = request.get('game_ids', [])

    if not email or not game_ids:
        return jsonify({'error': 'Faltan datos'}), 400

    return add(email, game_ids)

def get_library(email):
    return get(email)