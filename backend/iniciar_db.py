import os
import mysql.connector
from mysql.connector import Error
from steam_service import get_all_games_data
import json

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'ludoteca',
    'port': 3306
}

TABLAS = [
    "juegos",
    "generos",
    "juego_genero",
    "screenshots",
    "videos",
    "categorias",
    "juego_categoria",
    "requisitos_minimos",
    "requisitos_recomendados",
    "usuario"
    "biblioteca"
]

def connect_db():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(f"✅ Conexión exitosa a la base de datos '{DB_CONFIG['database']}'")
        return conn
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def ejecutar_init_db(connection):

    try:
        cursor = connection.cursor()
        with open("backend/init_db.sql", "r") as file:
            init_sql = file.read()

        sql_commands = [cmd.strip() for cmd in init_sql.split(';') if cmd.strip()]

        for command in sql_commands:
            try:
                if command: # Asegurarse de que el comando no esté vacío
                    cursor.execute(command)
                    # Si la sentencia es un SELECT o SHOW, puede haber resultados.
                    # Aunque para init_db.sql, generalmente no hay.
                    if cursor.with_rows:
                        cursor.fetchall() # Consumir resultados si los hay
                connection.commit() # Confirmar cada sentencia si es una modificación
            except Error as err:
                print(f"❌ Error al ejecutar una sentencia SQL: {command}")
                print(f"Error: {err}")
                connection.rollback() # Revertir si hay un error en una sentencia
        print("✅ Script init_db.sql ejecutado.")
    except FileNotFoundError:
        print("❌ Error: Archivo 'backend/init_db.sql' no encontrado.")
    except Error as e:
        print(f"❌ Error general al ejecutar init_db: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def generar_insert_sql(connection, name, data):
    if not data:
        print(f"No hay datos para insertar en la tabla '{name}'.")
        return

    cursor = connection.cursor()
    insert_count = 0
    error_count = 0

    for game in data:
        columns = []
        values = []

        for key, value in game.items():
            columns.append(key)

            if isinstance(value, str):
                # Escapar comillas simples correctamente para SQL
                values.append(f"'{value.replace("'", "''")}'")
            elif isinstance(value, (int, float)):
                values.append(str(value))
            elif isinstance(value, (list, dict)):
                # Convertir a JSON y escapar comillas simples dentro del JSON string
                json_str = json.dumps(value).replace("'", "''")
                values.append(f"'{json_str}'")
            elif value is None:
                values.append("NULL")
            else:
                # Caso por defecto, convertir a string y escapar
                values.append(f"'{str(value).replace("'", "''")}'")

        cols_str = ", ".join(columns)
        vals_str = ", ".join(values)

        insert_sql = f"INSERT INTO {name} ({cols_str}) VALUES ({vals_str});"
        try:
            cursor.execute(insert_sql)
            insert_count += 1
        except Error as err:
            print(f"❌ Error al ejecutar INSERT para el juego: {game.get('nombre', 'Desconocido')}")
            print(f"Sentencia: {insert_sql}")
            print(f"Error: {err}")
            error_count += 1

    connection.commit() # Confirmar todas las inserciones al final
    print(f"✅ Se intentaron insertar {insert_count + error_count} registros en '{name}'.")
    if error_count > 0:
        print(f"Se encontraron {error_count} errores durante la inserción.")
    cursor.close()

def clean_database(connection, db_name):

    if not connection or not connection.is_connected():
        print("❌ No hay una conexión activa al servidor MySQL para limpiar la base de datos.")
        return False

    try:
        with connection.cursor() as cursor: # Usamos un context manager para el cursor

            for table in TABLAS:
                try:
                    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM `{table}` LIMIT 1);")
                    result = cursor.fetchone()
                    if result and result[0]:  # Si hay al menos una fila
                        print(f"ℹ️ La tabla '{table}' contiene datos. No se eliminará la base de datos.")
                        return False
                except Error as e:
                    print(f"⚠️ No se pudo acceder a la tabla '{table}' (puede no existir): {e}")


            cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
            connection.commit()
            print(f"✅ Base de datos '{db_name}' eliminada porque estaba vacía.")
            return True

    except Error as e:
        print(f"❌ Error durante la limpieza y recreación de la base de datos '{db_name}': {e}")
        connection.rollback() # Revertir si hay un error
        return False

def init_db():
    conn = None
    try:
        conn = connect_db()
        if conn:
            if clean_database(conn, DB_CONFIG['database']):
                ejecutar_init_db(conn)
                print("\nObteniendo datos de juegos...")
                all_games_data = get_all_games_data()[0]# Esto debería devolver una lista de juegos
                if all_games_data:
                    generar_insert_sql(conn, "juegos", [g["game_info"] for g in all_games_data])
                    populate_tables(conn, all_games_data)
            else:
                print("No se obtuvieron datos de juegos para insertar.")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Conexión a la base de datos cerrada.")

def populate_tables(conn, all_games_data):
    cursor = conn.cursor()
    for game in all_games_data:
        game_id = game["game_info"]["id"]

        for genre in game["genres"]:
            cursor.execute(
                "INSERT IGNORE INTO generos (id_genero, descripcion) VALUES (%s, %s)",
                (genre["id"], genre["description"])
            )
            cursor.execute(
                "INSERT IGNORE INTO juego_genero (id_juego, id_genero) VALUES (%s, %s)",
                (game_id, genre["id"])
            )

        for category in game["categories"]:
            cursor.execute(
                "INSERT IGNORE INTO categorias (id, descripcion) VALUES (%s, %s)",
                (category["id"], category["description"])
            )
            cursor.execute(
                "INSERT IGNORE INTO juego_categoria (juego_id, categoria_id) VALUES (%s, %s)",
                (game_id, category["id"])
            )

        for screenshot in game["screenshots"]:
            cursor.execute(
                "INSERT INTO screenshots (juego_id, url) VALUES (%s, %s)",
                (game_id, screenshot["path_full"])
            )

        for video in game["videos"]:
            url = video.get("mp4", {}).get("max")
            if url:
                cursor.execute(
                    "INSERT INTO videos (juego_id, url) VALUES (%s, %s)",
                    (game_id, url)
                )
    conn.commit()
    cursor.close()