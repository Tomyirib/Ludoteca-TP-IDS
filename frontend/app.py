from flask import Flask, render_template, request, session, redirect, flash, url_for
import requests
from flask_cors import CORS
from flask_mail import Mail, Message
from blueprints.auth_routes import auth_bp
from blueprints.main_routes import main_bp
from blueprints.carrito_routes import carrito_bp
from blueprints.comunidad_routes import comunidad_bp
from blueprints.juegos_routes import juegos_bp
from config import BRAND, API_BASE

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ludotecavapor@gmail.com'
app.config['MAIL_PASSWORD'] = 'sloo scvg etsy txgw '

mail = Mail(app)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(comunidad_bp)
app.register_blueprint(juegos_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)