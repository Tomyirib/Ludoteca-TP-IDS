# Blueprint
# import dependencies
from flask import Blueprint, jsonify, request
from routes.database import get_db_connection
from mysql.connector import Error

# Define blueprint
users_bp = Blueprint("users", __name__)

# Queries
QUERY_ALL_USERS = "SELECT id_usuario, first_name, email, es_admin, created_at FROM usuario ORDER BY created_at DESC"
# Create routes

# get_all_users devuelve todos los usuarios de la base de datos
@users_bp.route("/all_users")
def get_all_users():
    """Retrieve all users for admin management"""
    connection = get_db_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = QUERY_ALL_USERS
        cursor.execute(query)
        users = cursor.fetchall()
        print("\nFROM BACKEND\n > users.py BP \n > GET_ALL_USERS, Users is of type: ", type(users), "\n")
        print("\nFROM BACKEND\n > users.py BP \n > GET_ALL_USERS, User is: ", users, "\n")
        return (users, 200)

    except Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()