from config.iniciar_db import connect_db as get_db_connection
import mysql

QUERY_ADD_USER = """
INSERT INTO usuario (email, contrasenia, first_name, last_name) VALUES (%s, %s, %s, %s)
"""

def add_user(email, password, first_name, last_name):
    conn = get_db_connection()
    if not conn:
        print("No se encontrado la base de datos")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(QUERY_ADD_USER, (email, password, first_name, last_name))
        conn.commit()
        print("Exitoso")
        return True

    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return "duplicado"
        print("duplicado")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name FROM usuario WHERE email = %s", (email,))
    user = cursor.fetchone()
    return user

def get_info(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, first_name, es_admin, email FROM usuario WHERE email = %s", (email,))
    user = cursor.fetchone()
    return user