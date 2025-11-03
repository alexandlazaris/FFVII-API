from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.materia import MateriaModel
from schemas import MateriaSchema, GetMateriaSchemaQueries
from game_data.materia.materia_data import materia_data
# from services.materia_service import filter_materia
import json
from flask import jsonify

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
        query = MateriaModel.query
        if query.count() == materia_data.__len__():
            print ('materia data has already been seeded, skipping', flush=True)
            abort(400)
        else:
            # TODO: below needs to be refactored, messy json handling
            dumps_json = json.dumps(materia_data)
            loaded_json = json.loads(dumps_json)
            for index in loaded_json:
                m = {
                    "name": index["name"],
                    "element": index["element"],
                    "type": index["type"],
                }
                materia = MateriaModel(**m)
                try:
                    db.session.add(materia)
                    db.session.commit()
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
    @blp.arguments(schema=GetMateriaSchemaQueries, location="query")
    def get(self, params):
        """
        Get materia data using optional filters for 'type' and 'element'.
        """
        query = MateriaModel.query
        if "type" in params:
            param = params["type"]
            if param != "":
                query = query.filter_by(type=param)

        if "element" in params:
            param = params["element"]
            if param != "":
                query = query.filter_by(element=param)
        return query.all()

    def delete(self):
        """
        Delete all materia.
        """
        count = MateriaModel.query.count()
        MateriaModel.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} materia"}
