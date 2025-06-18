
import repository.game_repository as game_repository
from flask import jsonify

def search_games(page, limit):
    result = game_repository.search_games(page, limit)
    print("asd")

def get_game_by_id(id):
    result = game_repository.get_game_by_id(id)

    if result is None:
        print("hacer algo")

    return result