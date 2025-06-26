# Admin
# Funciones auxiliares del FRONTEND se comunican a travez de la API con el backend

# dependencias
from flask import session, request, jsonify
import requests
from datetime import datetime

# ver si puede importar esta constante de un lugar mas general
API_BASE = 'http://backend:8080/'

# Hacer solo con session. no hace falta ir a la db
def is_user_admin():
    """Check if current user is admin"""
    if session.get('esta_logueado') and session.get('es_admin'):
        return True
    return False

    # user = get_user_by_id(session.get('user_id')) # from database
    # return user and user.get('is_admin', False)


# Aux Functions

# convierte string a datetime
def convert_datetime(value):
    return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z")

def get_users_for_admin():
    """Get all users with admin formatting"""
    users = get_all_users() # API Call to DB
    for user in users:
        user['created_at'] = convert_datetime(user['created_at'])
        user['role'] = 'Admin' if user.get('es_admin') else 'User'
        user['status'] = 'Active'  # Could be extended for user status
    return users

def get_user_for_admin(id_usuario):
    """Get all users with admin formatting"""
    user = get_user_by_id(id_usuario) # API Call to DB
    user['created_at'] = convert_datetime(user['created_at'])
    return user

def get_admin_dashboard_data():
    """Get data for admin dashboard"""
    return get_admin_stats() # API Call to DB

def admin_update_user(user_id, first_name, last_name, email, es_admin):
    """Admin function to update user details"""
    user_data = {"id_usuario" : user_id, "first_name" : first_name, "last_name": last_name, "email": email, "es_admin": es_admin}
    return update_user(user_data) # API Call to DB

def admin_delete_user(id_usuario):
    if id_usuario == session.get('usuario_id'):
        return {"status": "danger", "message" : "Cannot delete your own account"}
    return delete_user(id_usuario) # API Call to DB

# API CALLS

def get_all_users():
    """API CALL TO Retrieve all users"""
    response = requests.get(f'{API_BASE}/users/all_users')
    return response.json()

def get_admin_stats():
    """API CALL TO Retrieve admin stats"""
    response = requests.get(f'{API_BASE}/admin/admin_stats')
    return response.json()

def update_user(user_data):
    """API CALL TO Update user info"""
    response = requests.post(f'{API_BASE}/users/update_user', user_data)
    return response

def get_user_by_id(id_usuario):
    """API CALL TO Retrieve user data by ID"""
    response = requests.get(f'{API_BASE}/users/get_user/{id_usuario}')
    return response.json()

def delete_user(id_usuario):
    """API CALL TO Delete user data by ID"""
    print("\n admin.py frontend functions\nenter delete_user()\n")
    response = requests.post(f'{API_BASE}/users/delete_user/{id_usuario}')
    return response.json()