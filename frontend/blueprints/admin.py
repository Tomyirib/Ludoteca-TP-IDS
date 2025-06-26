from flask import Blueprint, url_for, request, render_template, flash, redirect, session
from utils.admin import is_user_admin, get_users_for_admin, get_admin_dashboard_data, admin_update_user, get_user_for_admin, admin_delete_user
admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/')
def dashboard():
    """Admin dashboard with statistics"""
    if not is_user_admin():
        flash("Need admin account to proceed", "danger")
        return redirect(url_for('login'))
    stats = get_admin_dashboard_data()
    return render_template('admin/dashboard.html', stats=stats)

# Manage Users
@admin_bp.route('/users')
def users():
    """Admin users management page"""
    user = []
    users = get_users_for_admin() # API to DB
    return render_template('admin/users.html', user=user, users=users)
# replace user=user with session['usuario_id'] line 63 in users.html


# Edit Users
@admin_bp.route('/users/<int:id_usuario>/edit', methods=['GET', 'POST'])
def edit_user(id_usuario):
    """Admin edit user page"""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        es_admin = 'es_admin' in request.form

        response = admin_update_user(id_usuario, first_name, last_name,email, es_admin)

        flash(response.json()['message'], response.json()['status'])

        if response.status_code == 200:
            return redirect(url_for('admin.users'))

    edit_user = get_user_for_admin(id_usuario)

    if edit_user['id_usuario'] == session['usuario_id']:
        flash('Cannot edit your own user', 'danger')
        return redirect(url_for('admin.users'))

    if not edit_user:
        flash('User not found', 'error')
        return redirect(url_for('admin.users'))

    return render_template('admin/edit_user.html', edit_user=edit_user)

# Delete User
@admin_bp.route('/users/<int:id_usuario>/delete', methods=['POST'])
def delete_user(id_usuario):
    """Admin delete user"""
    response = admin_delete_user(id_usuario)
    if type(response) == dict :
        flash(response['message'], response['status'])
    else:
        flash(response.json()['message'], response.json()['status'])

    return redirect(url_for('admin.users'))