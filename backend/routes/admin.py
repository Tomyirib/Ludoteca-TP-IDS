# Admin Blueprint
# import dependencies
from flask import Blueprint, jsonify, request
from iniciar_db import connect_db


# Define Blueprint
admin_bp = Blueprint("admin", __name__)

# Queries


# Routes
@admin_bp.route("/")
def admin():
    return