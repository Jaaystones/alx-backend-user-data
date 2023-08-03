#!usr/bin/env python3
"""
bycrypt encryption
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The salted and hashed password as a byte string.
    """
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password against a hashed password using bcrypt.

    Args:
        hashed_password (bytes): The salted and hashed password
        as a byte string.
        password (str): The plaintext password to be validated.

    Returns:
        bool: True if the password matches the hashed password.
        False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
