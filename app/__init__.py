from flask import Flask
import logging
from app.endpoints import api
from app.migrate import migrate_users_data


def create_app():
    app = Flask(__name__)
    app.config["RESTX_MASK_SWAGGER"] = False
    migrate_users_data()
    api.init_app(app)
    return app
