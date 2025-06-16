# Create Blueprint
from flask import Blueprint, jsonify

# import dependencies
from iniciar_db import connect_db

# Define my blueprint
comentarios_bp = Blueprint("comentarios", __name__)

# Queries
QUERY_RECIENTES = "SELECT comentarios.comentario_id, usuario.id_usuario, usuario.first_name AS usuario_username, juegos.id AS juego_id, juegos.name AS juego_nombre, comentarios.comentario_texto, juegos.header_image AS juego_imagen, comentarios.comentario_timestamp FROM comentarios INNER JOIN usuario ON comentarios.usuario_id=usuario.id_usuario INNER JOIN juegos ON comentarios.juego_id=juegos.id ORDER BY comentario_timestamp LIMIT 10"
QUERY_JUEGO = "SELECT comentarios.comentario_id, usuario.id_usuario, usuario.first_name AS usuario_username, juegos.id AS juego_id, juegos.name AS juego_nombre, comentarios.comentario_texto, juegos.header_image AS juego_imagen, comentarios.comentario_timestamp FROM comentarios INNER JOIN usuario ON comentarios.usuario_id=usuario.id_usuario INNER JOIN juegos ON comentarios.juego_id=juegos.id WHERE comentarios.juego_id = %s ORDER BY comentario_timestamp"


# Create the routes

# get_comentarios_recientes devuelve los 10 comentarios mas recientes
@comentarios_bp.route("/recientes")
def get_comentarios_recientes():
# def get_comentarios_recientes(cantidad):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_RECIENTES)
    # cursor.execute(QUERY_RECIENTES+"%s", (cantidad))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    if not comentarios:
        return ("No hay comentarios recientes", 404)
    return jsonify(comentarios)


# get_comentarios_juego devuelve los comentarios mas recientes del juego pasado
@comentarios_bp.route("/<int:juego_id>")
def get_comentarios_juego(juego_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_JUEGO, (juego_id,))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    if not comentarios:
        return (("No hay comentarios del juego %d", juego_id), 404)
    return jsonify(comentarios)