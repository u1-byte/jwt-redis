from flask_restx import Namespace, Resource, reqparse, fields
from http import HTTPStatus
import logging
from app.models import User

api = Namespace("Users", description="Users Endpoints", path="/users")

req_get = reqparse.RequestParser()
req_get.add_argument("username", type=str, required=True)

user_elm = api.model(
    "UserElm",
    {
        "id": fields.String(),
        "username": fields.String(),
        "city": fields.String(),
        "country": fields.String(),
        "role": fields.String(),
    },
)

resp_get = api.model(
    "UserGet",
    {
        "message": fields.String(),
        "result": fields.Nested(user_elm),
    },
)


@api.route("")
class GetUser(Resource):
    @api.expect(req_get)
    @api.marshal_with(resp_get)
    @api.doc(
        responses={
            HTTPStatus.UNAUTHORIZED.value: "User unauthorized for this content",
            HTTPStatus.NOT_FOUND.value: "User not found",
            HTTPStatus.INTERNAL_SERVER_ERROR.value: "Something went wrong",
        },
    )
    def get(self):
        try:
            res = req_get.parse_args()
            user = User.get(res["username"])
            if user is None:
                return {"message": "User not found."}, HTTPStatus.NOT_FOUND
            result = {
                "id": user.id,
                "username": user.username,
                "city": user.city,
                "country": user.country,
                "role": user.role,
            }
            return {"message": "Success", "result": result}
        except Exception as e:
            logging.error(f"{__name__} - {str(e)}")
            return {
                "message": "Something went wrong."
            }, HTTPStatus.INTERNAL_SERVER_ERROR
