#!/usr/bin/env python3
"""Module of Users views.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


def get_request_json():
    try:
        return request.get_json()
    except Exception:
        return None


def validate_create_user_data(data):
    if not data or not data.get("email") or not data.get("password"):
        return "Missing email or password"
    return None


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Return:
      - list of all User objects JSON represented.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
      - User ID.
    Return:
      - User object JSON represented.
      - 404 if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if not request.current_user:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
      - User ID.
    Return:
      - empty JSON is the User has been correctly deleted.
      - 404 if the User ID doesn't exist.
    """
    if not user_id:
        abort(404)
    user = User.get(user_id)
    if not user:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
      - email.
      - password.
      - last_name (optional).
      - first_name (optional).
    Return:
      - User object JSON represented.
      - 400 if can't create the new User.
    """
    data = get_request_json()
    error_msg = validate_create_user_data(data)
    if error_msg:
        return jsonify({'error': error_msg}), 400
    try:
        user = User(**data)
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
      - User ID.
    JSON body:
      - last_name (optional).
      - first_name (optional).
    Return:
      - User object JSON represented.
      - 404 if the User ID doesn't exist.
      - 400 if can't update the User.
    """
    if not user_id:
        abort(404)
    user = User.get(user_id)
    if not user:
        abort(404)
    data = get_request_json()
    if not data:
        return jsonify({'error': "Wrong format"}), 400
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    user.save()
    return jsonify(user.to_json()), 200
