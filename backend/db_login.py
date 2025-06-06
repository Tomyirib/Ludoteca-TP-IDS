from iniciar_db import connect_db
import mysql.connector
#funcion agregar usuarios a la db

def insert_user(email, contrasenia, first_name, last_name):
    conn = connect_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO usuario (email, contrasenia, first_name, last_name) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (email, contrasenia, first_name, last_name))
        conn.commit()
        return True
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return "duplicado"
        return False
    finally:
        cursor.close()
        conn.close()