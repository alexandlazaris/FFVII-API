from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.auth.auth import (
    SignUpRequestSchema,
    SignUpResponseSchema,
    LoginWithPasswordRequestSchema,
    LoginWithPasswordResponseSchema,
    LoginWithPasswordErrorSchema,
)
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
        request = SignupRequest.model_validate(body)
        try:
            response = signup_with_email_password(request.email, request.password)
            return response
        except EmailExistsError:
            abort(401, message="Email already exists")
        except EmailRateLimitExceededError:
            abort(
                500, message="Email send rate limit exceeded. Wait 2 hours & try again."
            )


@blp.route("login")
class LoginApi(MethodView):
    @blp.arguments(LoginWithPasswordRequestSchema)
    @blp.response(200, LoginWithPasswordResponseSchema)
    @blp.alt_response(401, schema=LoginWithPasswordErrorSchema)
    def post(self, body):
        """
        Login using existing email + password
        """
        request = LoginRequest.model_validate(body)
        try:
            session = login_with_password(request.email, request.password)
            return session.model_dump()
        except EmailNotConfirmedError:
            abort(401, message="Email not confirmed")
        except InvalidCredentialsError:
            abort(401, message="Invalid credentials")
