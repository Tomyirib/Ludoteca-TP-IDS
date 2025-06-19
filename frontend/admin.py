# Admin
# Funciones auxiliares del FRONTEND se comunican a travez de la API con el backend

# dependencias
from flask import session, request
import requests
from datetime import datetime

# ver si puede importar esta constante de un lugar mas general
API_BASE = 'http://localhost:8080/'

# Hacer solo con session. no hace falta ir a la db
# def is_admin_user():
#     """Check if current user is admin"""
#     if not session.get('logged_in'):
#         return False

#     user = get_user_by_id(session.get('user_id')) # from database
#     return user and user.get('is_admin', False)

# convierte string a datetime
def convert_datetime(value):
    return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z")

def get_users_for_admin():
    """Get all users with admin formatting"""
    users = get_all_users() # API Call to DB
    for user in users:
        print("\n\n", user['created_at'], "\n\n")
        user['created_at'] = convert_datetime(user['created_at'])
        user['role'] = 'Admin' if user.get('es_admin') else 'User'
        user['status'] = 'Active'  # Could be extended for user status
    return users


def get_all_users():
    """API CALL TO Retrieve all users fom BACKEND"""
    response = requests.get(f'{API_BASE}/users/all_users')
    return response.json()
