from repository.comments_repository import get_recents, get_comments_by_user, get_comments_by_game, add_comment, get_rating_by_game_id, get_comments_by_user

def get_recents_comments():
    return get_recents()

def get_comments_by_game(game_id):
    return get_comments_by_game(game_id)

def add_comment(request):
    data = request.form.to_dict()
    usuario_id = int(data.get("usuario_id").strip())
    juego_id = int(data.get("juego_id").strip())
    comentario_texto = data.get("comentario_texto").strip()
    rating = data.get("rating", "1").strip()  # Le pongo valor por defecto 0 REVISAR
    rating = int(rating)

    result = add_comment(usuario_id, juego_id, comentario_texto, rating)

    if result:
        return ("Comentario ingresado correctamente", 201)
    else:
        return ("Problema al guardar", 500)

def get_rating_by_game_id(game_id):
    return get_rating_by_game_id(game_id)

def get_comments_by_user(user_id):
    return get_comments_by_user(user_id)