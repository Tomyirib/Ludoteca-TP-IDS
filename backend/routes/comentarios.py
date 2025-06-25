# Blueprint
# import dependencies
from flask import Blueprint, jsonify, request
from iniciar_db import connect_db

# Define blueprint
comentarios_bp = Blueprint("comentarios", __name__)

# Queries
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

QUERY_ALL_COMMENTS = """
SELECT comentarios.comentario_id, usuario.id_usuario, usuario.first_name AS usuario_username,
       juegos.id AS juego_id, juegos.name AS juego_nombre,
       comentarios.comentario_texto, comentarios.rating,
       juegos.header_image AS juego_imagen,
       comentarios.comentario_timestamp
FROM comentarios
INNER JOIN usuario ON comentarios.usuario_id = usuario.id_usuario
INNER JOIN juegos ON comentarios.juego_id = juegos.id
ORDER BY comentario_timestamp DESC
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

INSERT_COMENTARIO = """
INSERT INTO comentarios (usuario_id, juego_id, comentario_texto, rating, comentario_timestamp)
VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
"""

# Create routes

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
        return ("No hay comentarios recientes", 204)
    return jsonify(comentarios)

# devuelve todos los comentarios
@comentarios_bp.route("/todos")
def get_all_comments_admin():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(QUERY_ALL_COMMENTS)
    comentarios = cursor.fetchall()
    connection.close()
    cursor.close()
    if not comentarios:
        return ("No hay comentarios recientes", 204)
    return jsonify(comentarios), 200

# get_comentarios_juego devuelve los comentarios mas recientes del juego pasado
@comentarios_bp.route("/juegos/<int:juego_id>")
def get_comentarios_juego(juego_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_JUEGO, (juego_id,))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    if not comentarios:
        return ("No hay comentarios para este juego", 204)
    return jsonify(comentarios)

# get_comentarios_usuario devuelve los comentarios mas recientes del usuario
@comentarios_bp.route("/usuario/<int:usuario_id>")
def get_comentarios_usuario(usuario_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_USUARIO, (usuario_id,))
    comentarios = cursor.fetchall()
    cursor.close()
    conn.close()
    if not comentarios:
        return ("No hay comentarios para este juego", 204)
    return jsonify(comentarios)

# Subir comentario a base de datos
@comentarios_bp.route("/ingresar_comentario", methods=["POST"])
def ingresar_comentario():
    # conneccion a db
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # armar Query con informacion recibida
    data = request.form.to_dict()
    usuario_id = int(data.get("usuario_id").strip())
    juego_id = int(data.get("juego_id").strip())
    comentario_texto = data.get("comentario_texto").strip()
    rating_str = data.get("rating")
    rating = data.get("rating", "1").strip()  #Le pongo valor por defecto 0 REVISAR
    rating = int(rating)

    # execute, commit and close
    cursor.execute(INSERT_COMENTARIO, (usuario_id, juego_id, comentario_texto, rating))
    conn.commit()
    cursor.close()
    conn.close()

    return ("Comentario ingresado correctamente", 201)