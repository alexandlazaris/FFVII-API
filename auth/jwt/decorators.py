from functools import wraps
from flask import g, request
from auth.jwt.verifier import verify_access_token
from auth.jwt.exceptions import InvalidTokenError

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise InvalidTokenError("Missing authorization header")

        if not auth_header.startswith("Bearer "):
            raise InvalidTokenError("Invalid authorization header")

        token = auth_header.removeprefix("Bearer ").strip()
        user = verify_access_token(token)
        g.user = user
        return func(*args, **kwargs)
    return wrapper