from flask.views import MethodView
from flask_smorest import Blueprint
from auth.jwt.decorators import require_auth
from services.saves_service import get_all_saves, delete_all_saves
import logging

from utils.responses import api_response

logger = logging.getLogger(__name__)

blp = Blueprint(
    "Saves",
    __name__,
    url_prefix="/saves",
    description="Managing a collection of save files",
)

# TODO: schema + model + logic + auth check needed
@blp.route("")
class SaveApi(MethodView):
    decorators = [require_auth]
    def get(self):
        """ 
        Get all save files including party info
        """
        body = get_all_saves()
        return api_response(body)

# TODO: schema + model + logic + auth check needed
    decorators = [require_auth]
    def delete(self):
        """
        Delete all save files
        """
        body = delete_all_saves()
        return api_response(body)