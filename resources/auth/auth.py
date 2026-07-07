from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.auth.auth import SignUpRequestSchema, SignUpResponseSchema
import logging
from services.auth.auth_service import *

logger = logging.getLogger(__name__)

blp = Blueprint(
    "Auth",
    __name__,
    url_prefix="/auth",
    description="Authentication for end users",
)

@blp.route("signup")
class SignupApi(MethodView):
    @blp.arguments(SignUpRequestSchema)
    @blp.response(201, SignUpResponseSchema)
    def post(self, body):
        """
        Sign up a new user with email + password
        """
        response = signup_with_email_password(body)
        return response

@blp.route("login")
class LoginApi(MethodView):
    def post(self):
        """
        Login using existing email + password
        """
        # dummy function at the moment, only prints
        response = {"result": "body"}
        return response