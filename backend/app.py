from flask import Flask
from controller.comments_controller import comentarios_bp
from controller.games_controller import games_bp
from controller.auth_controller import auth_bp
from controller.user_controller import user_bp
from controller.library_controller import library_bp

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

app.register_blueprint(comentarios_bp, url_prefix="/comments")
app.register_blueprint(games_bp, url_prefix="/games")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(library_bp, url_prefix="/library")
app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == '__main__':
    app.run(debug=True, port=8080)