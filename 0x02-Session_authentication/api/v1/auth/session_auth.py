#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from uuid import uuid4
from flask import request
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class.
    """
    def __init__(self):
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str) -> str:
        """Creates a session id for the user.
        """
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str) -> str:
        """Retrieves the user id of the user associated with
        a given session id.
        """
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Retrieves the user associated with the request.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id and session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
