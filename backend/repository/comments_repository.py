# import dependencies
from config.iniciar_db import connect_db
from flask import jsonify

QUERY_RECIENTES = """
SELECT comentarios.comentario_id, usuario.id_usuario, usuario.first_name AS usuario_username,
       juegos.id AS juego_id, juegos.name AS juego_nombre,
       comentarios.comentario_texto, comentarios.rating,
       juegos.header_image AS juego_imagen,
       comentarios.comentario_timestamp
FROM comentarios
INNER JOIN usuario ON comentarios.usuario_id = usuario.id_usuario
INNER JOIN juegos ON comentarios.juego_id = juegos.id
ORDER BY comentario_timestamp DESC
LIMIT 10
"""

QUERY_RATING_BY_GAME = """
                       SELECT AVG(rating) AS promedio
                       FROM comentarios
                       WHERE juego_id = %s
"""

QUERY_INSERT_COMMENT = """
INSERT INTO comentarios (usuario_id, juego_id, comentario_texto, rating, comentario_timestamp)
VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
"""

QUERY_JUEGO = """
SELECT comentarios.comentario_id, usuario.id_usuario, usuario.first_name AS usuario_username,
       juegos.id AS juego_id, juegos.name AS juego_nombre,
       comentarios.comentario_texto, comentarios.rating,
       juegos.header_image AS juego_imagen,
       comentarios.comentario_timestamp
FROM comentarios
INNER JOIN usuario ON comentarios.usuario_id = usuario.id_usuario
INNER JOIN juegos ON comentarios.juego_id = juegos.id
WHERE comentarios.juego_id = %s
ORDER BY comentario_timestamp DESC
"""

QUERY_USUARIO = """
SELECT comentarios.comentario_id, usuario.id_usuario, usuario.first_name AS usuario_username,
       juegos.id AS juego_id, juegos.name AS juego_nombre,
       comentarios.comentario_texto, comentarios.rating,
       juegos.header_image AS juego_imagen,
       comentarios.comentario_timestamp
FROM comentarios
INNER JOIN usuario ON comentarios.usuario_id = usuario.id_usuario
INNER JOIN juegos ON comentarios.juego_id = juegos.id
WHERE comentarios.usuario_id = %s
ORDER BY comentario_timestamp DESC
"""

def get_recents():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_RECIENTES)
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments

def get_comments_by_game(game_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_JUEGO, (game_id,))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    if not comentarios:
        return ("No hay comentarios para este juego", 204)
    return jsonify(comentarios)

def add_comment(usuario_id, juego_id, comentario_texto, rating):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(QUERY_INSERT_COMMENT, (usuario_id, juego_id, comentario_texto, rating))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        return False

def get_rating_by_game_id(game_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(QUERY_RATING_BY_GAME, (game_id,))
        result = cursor.fetchone()
        promedio = result[0] if result[0] is not None else 0
        return jsonify({'promedio': round(promedio, 1)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def get_comments_by_user(user):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_USUARIO, (user,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    if not comments:
        return ("No hay comentarios para este juego", 204)
    return jsonify(comments)