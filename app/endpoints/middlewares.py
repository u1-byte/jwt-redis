from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
import logging
from http import HTTPStatus
from functools import wraps
from app.models import User
from app.lib.redis_client import auth_client

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data: dict):
    identity = jwt_data["sub"]
    return User.get(identity["username"])


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_data: dict):
    jti = jwt_data["jti"]
    token_in_redis = auth_client.get(jti)
    return token_in_redis is not None


def admin_only():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt_identity()["role"]
            if role == "admin":
                return func(*args, **kwargs)
            return {
                "message": "Member cannot access this resource."
            }, HTTPStatus.FORBIDDEN

        return wrapper

    return decorator
