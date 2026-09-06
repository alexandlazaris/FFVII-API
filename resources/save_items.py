from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from auth.jwt.decorators import require_auth
from services.saves_service import get_save_by_id, delete_save_by_id, create_save
import logging

from utils.responses import api_response

logger = logging.getLogger(__name__)

blp = Blueprint(
    "Save item",
    __name__,
    url_prefix="/saves",
    description="Managing save files by id",
)


@blp.route("")
class SaveCreateApi(MethodView):
    decorators = [require_auth]
    def post(self):
        """
        Create a save file
        """
        body = request.get_json()
        save = create_save(body)
        return api_response(save)


@blp.route("<string:save_id>")
class SaveApi(MethodView):
    decorators = [require_auth]
    def get(self, save_id):
        """
        Get a save file by id
        """
        save = get_save_by_id(save_id)
        return api_response(save)

    decorators = [require_auth]
    def delete(self, save_id):
        """
        Delete a save file by id
        """
        body = delete_save_by_id(save_id)
        return api_response(body)
