from flask import jsonify
from config.iniciar_db import connect_db as get_db_connection

def add_library(email, game_ids):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        for game_id in game_ids:
            cursor.execute("INSERT IGNORE INTO biblioteca (user_email, game_id) VALUES (%s, %s)", (email, game_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Juegos agregados a biblioteca'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_library(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT g.*
            FROM biblioteca b
            JOIN juegos g ON b.game_id = g.id
            WHERE b.user_email = %s
        """, (email,))
        juegos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'juegos': juegos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

