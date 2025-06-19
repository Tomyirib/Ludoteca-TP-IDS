# Admin Blueprint
# import dependencies
from flask import Blueprint, jsonify, request, render_template
from admin import get_users_for_admin
from datetime import datetime
# Define Blueprint
admin_bp = Blueprint("admin", __name__)

# Queries

# Routes
# Dashboard
@admin_bp.route('/')
# @require_admin
def dashboard():
    """Admin dashboard with statistics"""
    # user = get_current_user()
    user = []
    # stats = get_admin_dashboard_data()
    stats = []
    return render_template('admin/dashboard.html', user=user, stats=stats)

# Manage Users
@admin_bp.route('/users')
# @require_admin
def users():
    """Admin users management page"""
    user = []
    users = get_users_for_admin() # API to DB
    return render_template('admin/users.html', user=user, users=users)

# Edit Users
@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
# @require_admin
def edit_user(user_id):
    """Admin edit user page"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        is_admin = 'is_admin' in request.form

        if admin_update_user(user_id, username, email, is_admin):
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.users'))
        else:
            flash('Error updating user', 'error')

    edit_user = get_user_by_id(user_id)
    current_user = get_current_user()

    if not edit_user:
        flash('User not found', 'error')
        return redirect(url_for('admin.users'))

    return render_template('admin/edit_user.html', user=current_user, edit_user=edit_user)