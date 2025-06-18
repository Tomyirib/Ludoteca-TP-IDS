from iniciar_db import connect_db as get_db_connection

QUERY_GET_BY_ID = """
SELECT 
        j.*, 
        c.descripcion AS categories,
        s.url AS screenshots,
        v.url AS videos
    FROM juegos j
    LEFT JOIN juego_categoria jc ON j.id = jc.juego_id
    LEFT JOIN categorias c ON jc.categoria_id = c.id
    LEFT JOIN screenshots s ON j.id = s.juego_id
    LEFT JOIN videos v ON j.id = v.juego_id
    WHERE j.id = %s
"""

QUERY_GET_ALL_GAMES = """
SELECT 
        j.*, 
    FROM juegos j
    LIMIT %s
    OFFSET %s
"""

QUERY_COUNT_TOTAL = """
    SELECT
    COUNT(*) as total
    FROM juegos
"""

def get_game_by_id(id):
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)
    cursor.execute(QUERY_GET_BY_ID, id)

    game = cursor.fetchAll()

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
