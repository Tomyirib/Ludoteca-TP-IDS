from flask import Blueprint, request
from service.user_service import get_user, get_user_info
user_bp = Blueprint("user", __name__)

@user_bp.route('/<email>', methods=['GET'])
def user_name(email):
    return get_user(email)

@user_bp.route('/info/<email>', methods=['GET'])
def user_info(email):
    return get_user_info(email)