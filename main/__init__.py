import os
import decimal
import flask.json
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_apispec.extension import FlaskApiSpec
import warnings


default_faceyelpdir = f"{os.getcwd()}/main/faceyelpapi.cfg"

docs = FlaskApiSpec()
db = SQLAlchemy()
cors = CORS()
api = Api()
jwt = JWTManager()


def read_config(config_filename=default_faceyelpdir):
  app = Flask(__name__)
  app.config.from_pyfile(config_filename)

  return app


class DecimalSerializeEncoder(flask.json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, decimal.Decimal):
      return float(obj)
    return super(DecimalSerializeEncoder, self).default(obj)


def create_app(config_filename=default_faceyelpdir):
  app = Flask(__name__)
  app.json_encoder = DecimalSerializeEncoder

  app.config.from_pyfile(config_filename)
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config.update({
      "APISPEC_SPEC": APISpec(
          title="FaceYelp API",
          version="0.1.0",
          openapi_version="2.0",
          plugins=[FlaskPlugin(), MarshmallowPlugin()]
      ),
      "APISPEC_SWAGGER_URL": "/docs.json",
      "APISPEC_SWAGGER_UI_URL": "/docs/"
  })

  # Register Extensions
  docs.init_app(app)
  db.init_app(app)
  cors.init_app(app)
  api.init_app(app)
  jwt.init_app(app)

  warnings.filterwarnings(
      "ignore",
      message="Multiple schemas resolved to the name ",
  )

  with app.app_context():
    # Blueprints
    from main.controllers.user import user_bp
    from main.controllers.friend import friend_bp
    # from main.controllers.meal import meal_bp
    from main.controllers.restaurant import restaurant_bp
    # from main.controllers.review import review_bp

    blueprints = [
        user_bp,
        friend_bp,
        # meal_bp,
        restaurant_bp,
        # review_bp,
    ]
    for bp in blueprints:
      app.register_blueprint(bp)

    docs.register_existing_resources()
    for key, value in docs.spec._paths.items():
      docs.spec._paths[key] = {
          inner_key: inner_value for inner_key, inner_value in value.items() if inner_key != "options"
      }

  return app
