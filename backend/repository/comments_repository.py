# import dependencies
from iniciar_db import connect_db

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

def get_recents():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_RECIENTES)
    # cursor.execute(QUERY_RECIENTES+"%s", (cantidad))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
def get_comments_by_game():
def add_comment():
def get_rating_by_game_id():