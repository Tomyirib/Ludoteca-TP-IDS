from user_service import add_user

def login(email, contrasenia):
    conn = connect_db()
    if not conn:
        return False

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, first_name, last_name, contrasenia FROM usuario WHERE email = %s", (email,))
    resultado = cursor.fetchone()

    if resultado and resultado['contrasenia'] == contrasenia:
        return resultado
    else:
        return False

def register(email, password, first_name, last_name):
    return add_user(email, password, first_name, last_name)