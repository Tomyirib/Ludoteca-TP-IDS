from flask import Blueprint, jsonify, request

library_bp = Blueprint("library", __name__)

@app.route('/biblioteca/agregar', methods=['POST'])
def agregar_a_biblioteca():
    data = request.get_json()
    email = data.get('email')
    game_ids = data.get('game_ids', [])

    if not email or not game_ids:
        return jsonify({'error': 'Faltan datos'}), 400

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

@app.route('/biblioteca/<email>', methods=['GET'])
def obtener_biblioteca(email):
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