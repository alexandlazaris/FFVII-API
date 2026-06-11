import os
from flask import Flask
from flask_smorest import Api
from resources.characters import blp as CharactersBlueprint
from resources.party import blp as PartyBlueprint
from resources.enemies import blp as EnemiesBlueprint
from resources.materia import blp as MateriaBlueprint
from resources.saves import blp as SavesBlueprint
from resources.health_check import blp as HealthCheckBlueprint
from db import db
from flask_migrate import Migrate
from flask_cors import CORS
from telemetry.logging_config import setup_logging
from telemetry.telemetry import telemetry 
import logging
logger = logging.getLogger(__name__)

def create_app(is_testing=False):
    logger.info('starting up app')
    app = Flask(__name__)
    CORS(app, methods=["GET", "POST", "PUT", "DELETE"])
    set_app_configs(app)
    set_db(app)
    register_api_routes(app)        
    if not is_testing:
        setup_logging()
        telemetry.initialise(app)
    else:
        logger.info ("skipping telemetry initialisations during testing")
    
    return app

def set_db(app):
    """
    Create & customise db settings.
    """
    logging.info('setting db values')
    db_url = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

def set_app_configs(app):
    logging.info('setting api configs')
    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "FF7 REST API"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

def register_api_routes(app):
    logging.info('registering api blueprints')
    api = Api(app)
    api.register_blueprint(CharactersBlueprint)
    api.register_blueprint(PartyBlueprint)
    api.register_blueprint(EnemiesBlueprint)
    api.register_blueprint(MateriaBlueprint)
    api.register_blueprint(SavesBlueprint)
    api.register_blueprint(HealthCheckBlueprint)
