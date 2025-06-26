# Blueprint
# import dependencies
from flask import Blueprint, request, jsonify
from routes.database import get_db_connection
from mysql.connector import Error

# Define blueprint
users_bp = Blueprint("users", __name__)

# Queries
QUERY_ALL_USERS = "SELECT id_usuario, first_name, email, es_admin, created_at FROM usuario ORDER BY created_at DESC"
QUERY_UPDATE_USER = "UPDATE usuario SET first_name = %s, last_name = %s, email = %s, es_admin = %s WHERE id_usuario = %s"
QUERY_USER_BY_ID = "SELECT * FROM usuario WHERE id_usuario = %s"
QUERY_DELETE_USER = "DELETE FROM usuario WHERE id_usuario = %s"

# Routes

# devuelve todos los usuarios de la base de datos
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
        return (users, 200)

    except Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# devuelve el usuario con id_usuario
@users_bp.route("/get_user/<int:id_usuario>")
def get_user_by_id(id_usuario):
    """Retrieve user data by ID"""
    connection = get_db_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(QUERY_USER_BY_ID, (id_usuario,))
        user = cursor.fetchone()
        return (user, 200)

    except Error as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Actualiza el usuario con la informacion pasada
@users_bp.route("/update_user/", methods=['POST'])
def update_user():
    """Update user information"""
    connection = get_db_connection()
    if connection is None:
        return False

    user_data = request.form.to_dict()
    cursor = connection.cursor()
    id_usuario = int(user_data.get("id_usuario").strip())
    first_name = user_data.get("first_name").strip()
    last_name = user_data.get("last_name").strip()
    email = user_data.get("email").strip()
    es_admin = (user_data.get("es_admin").strip() == 'True')

    try:
        cursor.execute(QUERY_UPDATE_USER, (first_name, last_name, email, es_admin, id_usuario))
        connection.commit()

        if cursor.rowcount == 0:
            result = {"status": "error", "message": f"User {id_usuario} not found"}, 404
        else:
            result = {"status": "success", "message": f"User {id_usuario} updated succesfully."}, 200

    except Error as e:
        result = {"error": str(e)}, 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        print("\nbackend > update_user: ", result, "\n")
        return jsonify(result[0]), result[1]

# Elimina el usuario con id_usuario
@users_bp.route("/delete_user/<int:id_usuario>", methods=['POST'])
def delete_user(id_usuario):
    """Delete a user"""
    connection = get_db_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(QUERY_DELETE_USER, (id_usuario,))
        connection.commit()
        if cursor.rowcount == 0:
            result = {"status": "error", "message": f"User {id_usuario} not found"}, 404
        else:
            result = {"status": "success", "message": f"User {id_usuario} deleted succesfully."}, 200

    except Error as e:
        result = {"error": str(e)}, 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        print("\nbackend > delete_user: ", result, "\n")
        return jsonify(result[0]), result[1]