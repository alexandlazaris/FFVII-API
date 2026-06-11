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

def create_app(is_testing=None):
    logger.info('starting up app')
    app = Flask(__name__)

    if is_testing is True:
        print ("skipping telemetry initialisations during testing")

    elif is_testing is False:
        setup_logging()
        telemetry.initialise(app)
        
    CORS(app, methods=["GET", "POST", "PUT", "DELETE"])
    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "FF7 REST API"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    logging.info('setting api configs')
    db_url = os.getenv("DATABASE_URL", "sqlite:///data.db")
    logging.info('starting db url')
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    logging.info('registering blueprints')
    api.register_blueprint(CharactersBlueprint)
    api.register_blueprint(PartyBlueprint)
    api.register_blueprint(EnemiesBlueprint)
    api.register_blueprint(MateriaBlueprint)
    api.register_blueprint(SavesBlueprint)
    api.register_blueprint(HealthCheckBlueprint)    
    return app
