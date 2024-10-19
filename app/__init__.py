from flask import Flask
import logging
from app.endpoints.middlewares import jwt
from app.endpoints import api
from app.migrate import migrate_users_data, empty_data
from app.env_load import (
    flask_env,
    jwt_algorithm,
    jwt_secret_key,
    jwt_refresh_exp,
    jwt_access_exp,
)


def create_app():
    app = Flask(__name__)
    logging.warning(
        f"Currently in {flask_env} env. Open docs at http://localhost:5000/docs"
    )
    # empty_data()
    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["JWT_ALGORITHM"] = jwt_algorithm
    app.config["JWT_SECRET_KEY"] = jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_access_exp
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = jwt_refresh_exp
    migrate_users_data()
    api.init_app(app)
    jwt.init_app(app)
    return app
