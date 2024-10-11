from flask_restx import Api
from app.endpoints.users import api as user_ns
from app.endpoints.login import api as login_ns
from app.endpoints.logout import api as logout_ns

api = Api(
    title="JWT Redis API",
    doc="/docs",
    description="API Documentation",
)

api.add_namespace(user_ns)
api.add_namespace(login_ns)
api.add_namespace(logout_ns)
