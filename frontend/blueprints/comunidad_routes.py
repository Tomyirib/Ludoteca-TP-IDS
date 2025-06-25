from flask import Blueprint, request, session, render_template, redirect, flash, url_for
import requests
from config import API_BASE, BRAND
from utils.utils import get_game, get_user_name, obtener_comentarios_juego, obtener_valoracion_promedio, obtener_comentarios_recientes, obtener_comentarios_usuario

comunidad_bp = Blueprint('comunidad', __name__)

@comunidad_bp.route('/juego/<int:game_id>', methods=['GET'])
def generic(game_id):
    nombre = None
    if 'email' in session:
        nombre = get_user_name(session['email'])
    juego = get_game(game_id)
    if juego:
        comentarios_juego = obtener_comentarios_juego(game_id)
        valoracion_promedio = obtener_valoracion_promedio(game_id)
        return render_template('endpoints/generic.html', juego=juego, comentarios_recientes=comentarios_juego, rating_prom=valoracion_promedio, nombre=nombre)
    else:
        return "Juego no encontrado", 404

@comunidad_bp.route('/comunidad')
def comunidad():
    comentarios_recientes = obtener_comentarios_recientes()
    comentarios_usuario = []
    if 'usuario_id' in session:
        comentarios_usuario = obtener_comentarios_usuario(session['usuario_id'])
    return render_template('endpoints/comunidad.html', brand=f"{BRAND} | Comunidad", comentarios_recientes=comentarios_recientes, comentarios_usuario=comentarios_usuario)

@comunidad_bp.route('/post_comentario', methods=["POST"])
def post_comentario():
    comentario_data = request.form.to_dict()
    comentario_data["usuario_id"] = "1"  # reemplazar luego con el real
    redirect_id = int(request.form["juego_id"])
    response = requests.post(f"{API_BASE}/comments/add", comentario_data)
    if response.status_code != 201:
        return "No se pudo ingresar comentario desde backend", 500
    return redirect(url_for('comunidad.generic', game_id=redirect_id))

@comunidad_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        try:
            nombre = request.form['name']
            mensaje = request.form['message']
            email = request.form['email']

            from app import mail
            from flask_mail import Message

            msg = Message(
                subject=f"Nuevo mensaje de {nombre}",
                sender='{email}',
                recipients=['ludotecavapor@gmail.com'],
                body=f"Remitente: {email}\n\n{mensaje}"
            )
            mail.send(msg)
            flash('✅ Email enviado con éxito.', 'success')
            return redirect(url_for('main.index'))

        except Exception as e:
            flash('❌ Error al enviar el email. Intente nuevamente.', 'error')
            return redirect(url_for('main.index'))

    return redirect(url_for('main.index'))