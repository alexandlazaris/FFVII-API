from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CharactersSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from models import CharactersModel
from db import db
import json

blp = Blueprint(
    "Characters",
    __name__,
    url_prefix="/characters",
    description="Read information about FF7 characters",
)


@blp.route("data")
class Characters(MethodView):
    @blp.response(201, CharactersSchema(many=True))
    def post(self):
        """
        Initialise characters into db.

        Perform this once.
        """
        dumps_json = json.dumps(characters)
        loaded_json = json.loads(dumps_json)
        for character in loaded_json:
            new_character = CharactersModel(**character)
            try:
                db.session.add(new_character)
                db.session.commit()
            #  TODO: add custom msg as to why it's 400
            except IntegrityError as e:
                abort(400, message=e.detail)
            except SQLAlchemyError():
                abort(500, message="Error occurred whilst inserting record.")
        return CharactersModel.query.all()
        

 
@blp.route("")
class Characters(MethodView):
    @blp.response(200, CharactersSchema(many=True))
    def get(self):
        """
        Get all character data.
        """
        try:
            return CharactersModel.query.all()
        except OperationalError:
            abort(500, message="Error fetching records.") 

    @blp.response(200)
    def delete(self):
        """
        Delete all characters.
        """
        count = CharactersModel.query.count()
        CharactersModel.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} characters"}


characters = [
    {"name": "Cloud", "weapon": "sword"},
    {"name": "Barret", "weapon": "machine gun"},
    {"name": "Tifa", "weapon": "physical"},
    {"name": "Aeris", "weapon": "staff"},
    {"name": "Red XIII", "weapon": "physical"},
    {"name": "Cait Sith", "weapon": "megaphone"},
    {"name": "Cid", "weapon": "spear"},
    {"name": "Vincent", "weapon": "rifle"},
    {"name": "Yuffie", "weapon": "shuriken"},
]
