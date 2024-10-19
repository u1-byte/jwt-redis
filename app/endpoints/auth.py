from flask_restx import Namespace, Resource, reqparse, fields
from http import HTTPStatus
import logging
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    get_jti,
)
from app.env_load import jwt_refresh_exp
from app.lib.redis_client import auth_client
from app.lib.pwd_util import is_password_match
from app.models import User

api = Namespace("Authentication", description="Auth Endpoints", path="/auth")

req = reqparse.RequestParser()
req.add_argument("username", type=str, required=True)
req.add_argument("password", type=str, required=True)

login_elm = api.model(
    "LoginElm",
    {
        "access_token": fields.String(),
        "refresh_token": fields.String(),
        "id": fields.String(),
        "username": fields.String(),
        "role": fields.String(),
    },
)

refresh_elm = api.model(
    "RefreshElm",
    {
        "access_token": fields.String(),
    },
)

login_resp = api.model(
    "LoginResp",
    {
        "message": fields.String(),
        "result": fields.Nested(login_elm),
    },
)

refresh_resp = api.model(
    "RefreshResp",
    {
        "message": fields.String(),
        "result": fields.Nested(refresh_elm),
    },
)


@api.route("/login")
class Login(Resource):
    @api.expect(req)
    @api.marshal_with(login_resp)
    @api.doc(
        responses={
            HTTPStatus.UNAUTHORIZED.value: "Wrong username or password",
            HTTPStatus.INTERNAL_SERVER_ERROR.value: "Something went wrong",
        },
    )
    def post(self):
        try:
            res = req.parse_args()
            user = User.get(res["username"])
            if user and is_password_match(res["password"], user.password):
                claims = {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                }
                result = claims.copy()
                refresh_token = create_refresh_token(identity=claims)
                claims["refresh_jti"] = get_jti(refresh_token)
                result["access_token"] = create_access_token(
                    identity=claims, fresh=True
                )
                result["refresh_token"] = refresh_token
                return {"message": "Success", "result": result}
            return {"message": "Wrong username or password."}, HTTPStatus.UNAUTHORIZED
        except Exception as e:
            logging.error(f"{__name__} - {str(e)}")
            return {
                "message": "Something went wrong."
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @api.marshal_with(refresh_resp)
    def post(self):
        try:
            claims = get_jwt_identity()
            access_token = create_access_token(identity=claims, fresh=False)
            return {"message": "Success", "result": {"access_token": access_token}}
        except Exception as e:
            logging.error(f"{__name__} - {str(e)}")
            return {
                "message": "Something went wrong."
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/logout")
class Logout(Resource):
    @jwt_required()
    def delete(self):
        try:
            claims = get_jwt_identity()
            access_jti = get_jwt().get("jti")
            refresh_jti = claims["refresh_jti"]
            auth_client.set(access_jti, "", ex=jwt_refresh_exp)
            auth_client.set(refresh_jti, "", ex=jwt_refresh_exp)
            return {"message": "Logged out."}
        except Exception as e:
            logging.error(f"{__name__} - {str(e)}")
            return {
                "message": "Something went wrong."
            }, HTTPStatus.INTERNAL_SERVER_ERROR
