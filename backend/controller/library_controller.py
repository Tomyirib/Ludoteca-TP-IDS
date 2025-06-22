from flask import Blueprint, jsonify, request
from service.library_service import add_library, get_library
library_bp = Blueprint("library", __name__)

@library_bp.route('/add', methods=['POST'])
def add_library():
    return add_library(request.get_json())

@library_bp.route('/<email>', methods=['GET'])
def get_library(email):
    return get_library(email)