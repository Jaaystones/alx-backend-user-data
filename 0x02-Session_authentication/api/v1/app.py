#!/usr/bin/env python3
"""Route module for the API.
"""
import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth, BasicAuth, SessionAuth,\
        SessionDBAuth, SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_options = {
    'auth': Auth,
    'basic_auth': BasicAuth,
    'session_auth': SessionAuth,
    'session_exp_auth': SessionExpAuth,
    'session_db_auth': SessionDBAuth,
}

auth_type = os.getenv('AUTH_TYPE', 'auth')
auth = auth_options.get(auth_type)


@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(403)
def error_handler(error):
    """Common error handler for 404, 401, and 403.
    """
    error_messages = {
        404: "Not found",
        401: "Unauthorized",
        403: "Forbidden",
    }
    message = error_messages.get(error.code, "An error occurred")
    return jsonify({"error": message}), error.code


@app.before_request
def authenticate_user():
    """Authenticates a user before processing a request.
    """
    if auth:
        excluded_paths = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
            "/api/v1/auth_session/login/",
        ]
        if auth.require_auth(request.path, excluded_paths):
            user = auth.current_user(request)
            if not auth.authorization_header(request)\
                    and not auth.session_cookie(request):
                abort(401)
            if not user:
                abort(403)
            request.current_user = user


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
