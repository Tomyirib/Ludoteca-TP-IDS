# Admin Blueprint
# import dependencies
from flask import Blueprint, url_for, request, render_template, flash, redirect
from admin import get_users_for_admin, get_admin_dashboard_data, admin_update_user, get_user_for_admin, admin_delete_user
# Define Blueprint
admin_bp = Blueprint("admin", __name__)

# Queries

# Routes
# Dashboard
@admin_bp.route('/')
# @require_admin
def dashboard():
    """Admin dashboard with statistics"""
    stats = get_admin_dashboard_data()
    return render_template('admin/dashboard.html', stats=stats)

# Manage Users
@admin_bp.route('/users')
# @require_admin
def users():
    """Admin users management page"""
    user = []
    users = get_users_for_admin() # API to DB
    return render_template('admin/users.html', user=user, users=users)
# replace user=user with session['usuario_id'] line 63 in users.html


# Edit Users
@admin_bp.route('/users/<int:id_usuario>/edit', methods=['GET', 'POST'])
# @require_admin
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

    if not edit_user:
        flash('User not found', 'error')
        return redirect(url_for('admin.users'))

    return render_template('admin/edit_user.html', edit_user=edit_user)

# Delete User
@admin_bp.route('/users/<int:id_usuario>/delete', methods=['POST'])
# @require_admin
def delete_user(id_usuario):
    """Admin delete user"""
    response = admin_delete_user(id_usuario)
    print("\n admin.py frontend routes\n response: ", response,"\n")
    print("\n admin.py frontend routes\n response type: ", type(response),"\n")
    if type(response) == dict :
        flash(response['message'], response['status'])
    else:
        flash(response.json()['message'], response.json()['status'])

    return redirect(url_for('admin.users'))