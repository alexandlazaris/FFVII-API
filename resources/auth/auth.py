from flask.views import MethodView
from flask_smorest import Blueprint, abort
from auth.auth_exceptions import *
from auth.jwt.decorators import require_auth
from schemas.auth.auth import (
    SignUpRequestSchema,
    SignUpResponseSchema,
    LoginWithPasswordRequestSchema,
    LoginWithPasswordResponseSchema,
    LoginWithPasswordErrorSchema,
    LogoutSchema,
    SignupConfirmEmailToken
)
from models.auth.auth import (
    SignupRequest,
    LoginRequest,
    SignUpConfirmRequest,
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
    @blp.response(200, SignUpResponseSchema)
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
            return session
        except EmailNotConfirmedError:
            abort(401, message="Email not confirmed")
        except InvalidCredentialsError:
            abort(401, message="Invalid credentials")


# TODO: add token_hash as a query param, remove from payload, e.g. ?token_hash=123
@blp.route("confirm")
class ConfirmApi(MethodView):
    @blp.arguments(SignupConfirmEmailToken)
    def post(self, body):
        """
        Confirm signup invite for new user
        """
        request = SignUpConfirmRequest.model_validate(body)
        try:
            response = confirm_user_sign(token_hash=request.token_hash)
            return response
        except SignUpInviteExpiredError:
            abort(401, message="Confirmation link has expired. Signup again.")
        except SignUpInviteDisabledError:
            abort(404, message="Signup through email has been disabled for this app.")


# @require_auth
@blp.route("logout")
class LogoutApi(MethodView):
    decorators = [require_auth]

    @blp.response(204, LogoutSchema)
    def post(self):
        """
        Logout of existing session
        """
        try:
            session = sign_out()
            return session
        except SessionNotFound:
            abort(401, message="User session not found")
