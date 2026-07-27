from flask.views import MethodView
from flask_smorest import Blueprint
from auth.jwt.decorators import require_auth
from schemas import SaveRequestSchema, SaveResponseSchema
from services.saves_service import get_save_by_id, delete_save_by_id, create_save
from flask import g
import logging

logger = logging.getLogger(__name__)

blp = Blueprint(
    "Save item",
    __name__,
    url_prefix="/save",
    description="Managing save files by id",
)

@blp.route("")
class SaveCreateApi(MethodView):
    @require_auth
    @blp.arguments(SaveRequestSchema)
    @blp.response(201, SaveResponseSchema)
    def post(self, body):
        """
        Create a save file
        """
        return create_save(body)


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