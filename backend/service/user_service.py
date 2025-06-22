from flask import Blueprint, jsonify
from repository.user_repository import add_user as add
from repository.user_repository import get_info

#TODO move to repository
def add_user(email, password, first_name, last_name):
    add(email, password, first_name, last_name)

def get_user(email):
    user = get_user(email)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

def get_user_info(email):
    user = get_info(email)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404