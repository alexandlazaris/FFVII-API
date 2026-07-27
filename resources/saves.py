from flask.views import MethodView
from flask_smorest import Blueprint
from auth.jwt.decorators import require_auth
from schemas import SaveResponseSchema
from services.saves_service import get_all_saves, delete_all_saves
from flask import g
import logging

logger = logging.getLogger(__name__)

blp = Blueprint(
    "Saves",
    __name__,
    url_prefix="/saves",
    description="Managing a collection of save files",
)

@blp.route("")
class SaveApi(MethodView):
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