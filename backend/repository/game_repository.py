from config.iniciar_db import connect_db as get_db_connection
from flask import jsonify

QUERY_GET_BY_ID = """
SELECT * FROM juegos WHERE id = %s
"""

QUERY_GET_GENDERS = """
                   SELECT g.descripcion
                   FROM generos g
                            JOIN juego_genero jg ON g.id_genero = jg.id_genero
                   WHERE jg.id_juego = %s
                   """

QUERY_GET_CATEGORIES = """
                   SELECT c.descripcion
                   FROM categorias c
                            JOIN juego_categoria jc ON c.id = jc.categoria_id
                   WHERE jc.juego_id = %s
                   """

QUERY_GET_URL = "SELECT url FROM screenshots WHERE juego_id = %s"

QUERY_GET_VIDEOS = "SELECT url FROM videos WHERE juego_id = %s"

QUERY_GET_ALL_GAMES = """
SELECT j.* FROM juegos j LIMIT %s OFFSET %s
"""

QUERY_COUNT_TOTAL = """
    SELECT
    COUNT(*) as total
    FROM juegos
"""

def get_game_by_id(id):
    connection = get_db_connection()

    if not connection:
        print("No database connection")

    cursor = connection.cursor(dictionary=True)

    cursor.execute(QUERY_GET_BY_ID, (id,))
    game = cursor.fetchone()

    cursor.execute(QUERY_GET_GENDERS, (id,))
    generos = cursor.fetchall()

    cursor.execute(QUERY_GET_CATEGORIES, (id,))
    categories = cursor.fetchall()

    cursor.execute(QUERY_GET_URL, (id,))
    screenshots = cursor.fetchall()

    cursor.execute(QUERY_GET_VIDEOS, (id,))
    videos = cursor.fetchall()

    game["generos"] = generos
    game['categories'] = categories
    game['screenshots'] = screenshots
    game['videos'] = videos

    close_connection(cursor, connection)

    if not game:
        return None
    return game

def search_games(page, limit):
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(QUERY_GET_ALL_GAMES, (limit, offset))
    games = cursor.fetchall()

    cursor.execute(QUERY_COUNT_TOTAL)
    totalCount = cursor.fetchone()["total"]

    return (games, totalCount)

def close_connection(cursor, connection):
    cursor.close()
    connection.close()
