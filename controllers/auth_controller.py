# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
import logging

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# Set up logger (re-use your app logger)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == '1234':
        # Placeholder for JWT token generation (future step)
        response = {
            "message": "Login successful",
            "token": None  # to be replaced with JWT in future
        }
        logger.info(f"Successful login attempt by user '{username}'")
        return jsonify(response), 200
    else:
        logger.warning(f"Failed login attempt for user '{username}'")
        return jsonify({"message": "Invalid credentials"}), 401
