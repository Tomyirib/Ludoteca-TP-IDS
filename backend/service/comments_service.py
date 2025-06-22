from comments_repository import get_recents

def get_recents_comments():
    return get_recents()

def get_comments_by_game(game_id):
    return get_comments_by_game(game_id)

def add_comment(request):
    data = request.form.to_dict()
    usuario_id = int(data.get("usuario_id").strip())
    juego_id = int(data.get("juego_id").strip())
    comentario_texto = data.get("comentario_texto").strip()
    rating_str = data.get("rating")
    rating = data.get("rating", "1").strip()  # Le pongo valor por defecto 0 REVISAR
    rating = int(rating)

    result = add_comment(usuario_id, juego_id, comentario_texto, rating)

    if result:
        return ("Comentario ingresado correctamente", 201)
    else:
        return ("Problema al guardar", 500)

def get_rating_by_game_id(game_id):
    return get_rating_by_game_id(game_id)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT AVG(rating) AS promedio
                       FROM comentarios
                       WHERE juego_id = %s
                       """, (game_id,))
        result = cursor.fetchone()
        promedio = result[0] if result[0] is not None else 0
        return jsonify({'promedio': round(promedio, 1)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()