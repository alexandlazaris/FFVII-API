import os
from flask import Flask
from flask_smorest import Api
from resources.characters import blp as CharactersBlueprint
from resources.party import blp as PartyBlueprint
from resources.enemies import blp as EnemiesBlueprint
from resources.materia import blp as MateriaBlueprint
from resources.saves import blp as SavesBlueprint
from db import db
from flask_migrate import Migrate
from dotenv import load_dotenv


def create_app(db_url=None):
    app = Flask(__name__)
        
    load_dotenv()    
    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "FF7 REST API"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    
    db_url = os.getenv("DATABASE_URL", "sqlite:///data.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(CharactersBlueprint)
    api.register_blueprint(PartyBlueprint)
    api.register_blueprint(EnemiesBlueprint)
    api.register_blueprint(MateriaBlueprint)
    api.register_blueprint(SavesBlueprint)

    return app
