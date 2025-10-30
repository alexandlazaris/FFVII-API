from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.materia import MateriaModel
from schemas import MateriaSchema
from game_data.materia.materia_data import materia_data
import json

blp = Blueprint(
    "Materia",
    __name__,
    url_prefix="/materia",
    description="Assign materia to party members",
)


@blp.route("data")
class Materia(MethodView):
    @blp.response(201, MateriaSchema(many=True))
    def post(self):
        """
        Initialise game materia into db.

        Perform this once.
        """
        # TODO: review this dump, seems unnecessary
        dumps_json = json.dumps(materia_data)
        loaded_json = json.loads(dumps_json)
        for index in loaded_json:
            m = {
                "name": index['name'],
                "element": index['element'],
                "type": index['type'],
            }
            materia = MateriaModel(**m)
            try:
                db.session.add(materia)
                db.session.commit()
            #  TODO: add custom msg as to why it's 400
            except IntegrityError as e:
                abort(400, message=e._message)
            except SQLAlchemyError():
                abort(500, message="Error occurred whilst inserting record.")
        return MateriaModel.query.all()


@blp.route("")
class Materia(MethodView):
    @blp.arguments(MateriaSchema(many=True))
    @blp.response(201, MateriaSchema(many=True))
    def post(self, request):
        """
        Add materia.
        """
        response = []
        for m in request:
            materia = MateriaModel(**m)
            response.append(materia)
        try:
            db.session.add_all(response)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError():
            abort(500, message="Error occurred whilst inserting record.")
        return response

    @blp.response(200, MateriaSchema(many=True))
    def get(self):
        """
        Get all available materia information.
        """
        return MateriaModel.query.all()

    def delete(self):
        """
        Delete all materia.
        """
        count = MateriaModel.query.count()
        MateriaModel.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} materia"}
    