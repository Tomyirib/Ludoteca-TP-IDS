from iniciar_db import connect_db as get_db_connection

QUERY_GET_USER_BY_EMAIL = """
SELECT id_usuario, first_name, last_name, contrasenia FROM usuario WHERE email = %s
"""


def get_user_by_email(email, password):
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)
    cursor.execute(QUERY_GET_USER_BY_EMAIL, (email,))
    user = cursor.fetchone()

    if user and user['contrasenia'] == password:
        return user
    else:
        return False