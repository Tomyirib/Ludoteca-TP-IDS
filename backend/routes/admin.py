# Blueprint
# import dependencies
from flask import Blueprint
from routes.database import get_db_connection
from mysql.connector import Error

# Define blueprint
admin_bp = Blueprint("admin", __name__)

# Queries
QUERY_TOTAL_USERS = "SELECT COUNT(*) as total_users FROM usuario"
QUERY_ADMIN_USERS = "SELECT COUNT(*) as admin_users FROM usuario WHERE es_admin = 1"
QUERY_TOTAL_GAMES = "SELECT COUNT(*) as total_games FROM juegos"
QUERY_TOTAL_GENRES = "SELECT COUNT(*) as total_genres FROM generos"
QUERY_TOTAL_COMMENTS = "SELECT COUNT(*) as total_comments FROM comentarios"
QUERY_RECENT_USERS = """
SELECT COUNT(*) as recent_users
FROM usuario
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
"""
QUERY_RECENT_COMMENTS = """
SELECT COUNT(*) as recent_comments
FROM comentarios
WHERE comentario_timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
"""

# Routes

@admin_bp.route("/admin_stats")
def get_admin_stats():
    """Get statistics for admin dashboard"""

    connection = get_db_connection()
    if connection is None:
        return {}

    try:
        cursor = connection.cursor(dictionary=True)

        # Get user stats
        cursor.execute(QUERY_TOTAL_USERS)
        total_users = cursor.fetchone()['total_users']

        cursor.execute(QUERY_ADMIN_USERS)
        admin_users = cursor.fetchone()['admin_users']

        # Get game stats
        cursor.execute(QUERY_TOTAL_GAMES)
        total_games = cursor.fetchone()['total_games']

        cursor.execute(QUERY_TOTAL_GENRES)
        total_genres = cursor.fetchone()['total_genres']

        # Get comment stats
        cursor.execute(QUERY_TOTAL_COMMENTS)
        total_comments = cursor.fetchone()['total_comments']

        # Get recent activity
        cursor.execute(QUERY_RECENT_USERS)
        recent_users = cursor.fetchone()['recent_users']

        cursor.execute(QUERY_RECENT_COMMENTS)
        recent_comments = cursor.fetchone()['recent_comments']

        return {
            'total_users': total_users,
            'admin_users': admin_users,
            'total_games': total_games,
            'total_genres': total_genres,
            'regular_users': total_users - admin_users,
            'total_comments': total_comments,
            'recent_users': recent_users,
            'recent_comments': recent_comments
        }
    except Error as e:
        print(f"Error getting admin stats: {e}")
        return {}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
