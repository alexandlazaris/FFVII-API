from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models.materia import MateriaModel
from schemas import MateriaSchema, GetMateriaSchemaQueries
from services.materia_service import get_materia_with_filters, seed_materia_data

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
        Initialise game materia into db, perform this once.
        """
        return seed_materia_data()


@blp.route("")
class Materia(MethodView):
    @blp.response(200, MateriaSchema(many=True))
    @blp.arguments(schema=GetMateriaSchemaQueries, location="query")
    def get(self, params):
        """
        Get materia data using query params for filters.
        """
        return get_materia_with_filters(params)

    def delete(self):
        """
        Delete all materia.
        """
        count = MateriaModel.query.count()
        MateriaModel.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} materia"}
