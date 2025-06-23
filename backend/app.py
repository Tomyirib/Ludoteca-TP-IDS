from flask import Flask
from flask_cors import CORS
from config.iniciar_db import init_db
from controller.comments_controller import comments_bp
from controller.games_controller import games_bp
from controller.auth_controller import auth_bp
from controller.user_controller import user_bp
from controller.library_controller import library_bp

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
CORS(app)

app.register_blueprint(comments_bp, url_prefix="/comments")
app.register_blueprint(games_bp, url_prefix="/games")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(library_bp, url_prefix="/library")
app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=8080)