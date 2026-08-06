from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import g
from auth.jwt.decorators import require_auth
from schemas.user.user import GetUserResponse, GetUserNotFoundSchema
import logging
from services.user.user_service import get_profile
from auth.user_exceptions import *

logger = logging.getLogger(__name__)

blp = Blueprint("User", __name__, url_prefix="/user")


@blp.route("profile")
class ProfileApi(MethodView):
    decorators = [require_auth]

    @blp.response(200, GetUserResponse)
    @blp.alt_response(401, schema=GetUserNotFoundSchema)
    def get(self):
        """
        Get user profile
        """
        try:
            user = get_profile(g.access_token)
            return user
        except UserNotFound:
            abort(401, message="User session not found")
