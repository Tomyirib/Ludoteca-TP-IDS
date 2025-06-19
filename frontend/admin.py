from flask import session
# from database import get_user_by_id

def is_admin_user():
    """Check if current user is admin"""
    if not session.get('logged_in'):
        return False

    user = get_user_by_id(session.get('user_id')) # from database
    return user and user.get('is_admin', False)