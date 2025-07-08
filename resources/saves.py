from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import SaveRequestSchema, SaveResponseSchema
from services.saves_service import get_all_saves, create_save, delete_all_saves, get_save_by_id, delete_save_by_id


blp = Blueprint(
    "Save",
    __name__,
    url_prefix="/saves",
    description="CRUD for save files",
)


@blp.route("")
class SaveApi(MethodView):
    @blp.arguments(SaveRequestSchema)
    @blp.response(201, SaveResponseSchema)
    def post(self, body):
        """
        Create a save file
        """
        return create_save(body)

    @blp.response(200, SaveResponseSchema(many=True))
    def get(self):
        """ 
        Get all save files with party info
        """
        return get_all_saves()

    @blp.response(200)
    def delete(self):
        """
        Delete all save files
        """
        return delete_all_saves()

@blp.route("<string:id>")
class SaveApi(MethodView):
    @blp.response(200, SaveResponseSchema)
    def get(self, id):
        """
        Get a save file by id
        """
        return get_save_by_id(id)
    
    @blp.response(200)
    def delete(self, id):
        """
        Delete a save file by id
        """
        return delete_save_by_id(id)