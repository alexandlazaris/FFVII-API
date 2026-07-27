from flask import jsonify
from auth.jwt.exceptions import InvalidTokenError


def register_auth_handlers(app):
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(error):
        return jsonify({
            "error": "Invalid or missing authentication token"
        }), 401