from flask import Blueprint, jsonify
from repository.user_repository import add_user as add

#TODO move to repository
def add_user(email, password, first_name, last_name):
    add(email, password, first_name, last_name)

def get_user(email):
    user = get_user(email)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404