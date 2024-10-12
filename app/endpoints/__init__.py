from flask_restx import Api
import logging
from jwt import PyJWTError
from http import HTTPStatus
from flask_jwt_extended.exceptions import JWTExtendedException
from app.endpoints.users import api as user_ns
from app.endpoints.auth import api as auth_ns

authorizations = {
    "tokenkey": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    title="JWT Redis API",
    doc="/docs",
    description="API Documentation",
    security="tokenkey",
    authorizations=authorizations,
)

api.add_namespace(user_ns)
api.add_namespace(auth_ns)


@api.errorhandler(PyJWTError)
def jwt_error_handler(e):
    logging.error(f"{__name__} - {str(e)}")
    message = "Token is not valid."
    return {"message": message}, HTTPStatus.UNAUTHORIZED


@api.errorhandler(JWTExtendedException)
def jwt_extended_error_handler(e):
    logging.error(f"{__name__} - {str(e)}")
    message = "Token is not valid."
    return {"message": message}, HTTPStatus.UNAUTHORIZED
