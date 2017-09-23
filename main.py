import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from app import models
from config import app_configuration
# from app.views.assets import AssetResource


def create_app(environment):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configuration[environment])
    models.db.init_app(app)
    migrate = Migrate(app,models.db)
    api = Api(app)
    # api.add_resource(AssetResource,
    #                  '/api/v1/assets', '/api/v1/assets/',
    #                  endpoint='assets')
    return app

app = create_app(os.getenv("FLASK_CONFIG"))

if __name__ == "__main__":
    environment = os.getenv("FLASK_CONFIG")
    app = create_app(environment)
    app.run()
