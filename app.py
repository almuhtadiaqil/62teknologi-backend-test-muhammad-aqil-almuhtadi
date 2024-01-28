from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from argparse import ArgumentParser
import os

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["JSON_SORT_KEYS"] = False

jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app=app, db=db)

from controllers.auth_controller import auth_api
from controllers.business_controller import business_api

prefix = "/api"
app.register_blueprint(auth_api, url_prefix=prefix)
app.register_blueprint(business_api, url_prefix=prefix + "/business")
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="Port to listen on"
    )
    args = parser.parse_args()
    port = args.port
    app.run()
