from flask import Blueprint, render_template, request, redirect, session, flash, url_for
import requests
from utils.utils import get_user_name, get_user_info
from config import BRAND, API_BASE

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    if request.method == 'POST':
        data = {
            'email_login': request.form['email_login'],
            'password_login': request.form['password_login']
        }
        resp = requests.post('http://backend:8080/auth/login', data=data)
        if resp.status_code == 200:
            session['email'] = request.form['email_login']
            user = get_user_info(session['email'])
            session['first_name'] = user['first_name']
            session['es_admin'] = user['es_admin']
            session['esta_logueado'] = True
            session['usuario_id'] = user['id_usuario']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.index'))
        else:
            mensaje = resp.json().get('error', 'Usuario o contraseña incorrectos')
            flash(mensaje, 'danger')
            return render_template('endpoints/login.html', brand=BRAND, nombre=nombre)
    return render_template('endpoints/login.html', brand=BRAND, nombre=nombre)

@auth_bp.route('/register', methods=['GET', 'POST'])

def register():
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    if request.method == 'POST':
        data = {
            'email_signup': request.form['email_signup'],
            'password_signup': request.form['password_signup'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name']
        }
        resp = requests.post('http://backend:8080/auth/register', data=data)
        if resp.status_code == 201:
            flash('Registro exitoso. Ya podés iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            mensaje = resp.json().get('error', 'Error al registrar usuario. Por favor, intente nuevamente.')
            flash(mensaje, 'danger')
    return render_template('endpoints/login.html', brand=BRAND, nombre=nombre)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('main.index'))
