from flask import Blueprint, request
from service.user_service import get_user
user_bp = Blueprint("user", __name__)

@user_bp.route('/user/<email>', methods=['GET'])
def get_user(email):
    return get_user(email)