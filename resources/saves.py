from flask.views import MethodView
from flask_smorest import Blueprint
from auth.decorators import require_auth
from schemas import SaveRequestSchema, SaveResponseSchema
from services.saves_service import get_all_saves, create_save, delete_all_saves, get_save_by_id, delete_save_by_id
from flask import g

blp = Blueprint(
    "Save",
    __name__,
    url_prefix="/saves",
    description="CRUD for save files",
)

@blp.route("")
class SaveApi(MethodView):
    @require_auth
    @blp.arguments(SaveRequestSchema)
    @blp.response(201, SaveResponseSchema)
    def post(self, body):
        """
        Create a save file
        """
        return create_save(body)

    @require_auth
    @blp.response(200, SaveResponseSchema(many=True))
    def get(self):
        """ 
        Get all save files including party info
        """
        print(f"user_id: {g}", flush=True)
        return get_all_saves()

    @require_auth
    @blp.response(200)
    def delete(self):
        """
        Delete all save files
        """
        return delete_all_saves()

@blp.route("<string:id>")
class SaveApi(MethodView):
    @require_auth
    @blp.response(200, SaveResponseSchema)
    def get(self, id):
        """
        Get a save file by id
        """
        return get_save_by_id(id)
    
    @require_auth
    @blp.response(200)
    def delete(self, id):
        """
        Delete a save file by id
        """
        return delete_save_by_id(id)