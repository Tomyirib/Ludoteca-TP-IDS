import requests
from utils.config import API_BASE

def get_user_info(email):
    resp = requests.get(f'http://backend:8080/user/info/{email}')
    if resp.status_code == 200:
        return resp.json()
    return None

def get_user_name(email):
    resp = requests.get(f'http://backend:8080/user/{email}')
    if resp.status_code == 200:
        return resp.json().get('first_name')
    return None

def get_game(game_id):
    response = requests.get(f"http://backend:8080/games/{game_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def obtener_comentarios_recientes():
    response = requests.get(f"{API_BASE}/comments/recents")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_valoracion_promedio(game_id):
    response = requests.get(f"{API_BASE}/comments/rating/{game_id}")
    if response.status_code == 200:
        return response.json().get('promedio', 0)
    return 0

def obtener_comentarios_juego(juego_id):
    response = requests.get(f"{API_BASE}/comments/{juego_id}")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_comentarios_usuario(usuario_id):
    response = requests.get(f"{API_BASE}/comments/user/{usuario_id}")
    if response.status_code == 200:
        return response.json()
    return []