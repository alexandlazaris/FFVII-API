from flask_smorest import abort
from pydantic import ValidationError
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.auth.auth import Signup
import json
from flask import jsonify
import logging
from auth.auth_client import auth

logger = logging.getLogger(__name__)


def signup_with_email_password(body):
    try:
        logger.info("validating new user")
        request_validated = Signup.model_validate(body)
        # TODO: make a model for the return sign up response
        response = auth.signup(request_validated.email, request_validated.password)
    except ValidationError:
        abort(400, message="Invalid request. Validation failed for email/password")
    return response

# TODO:
# make a login function
# make a logout function
# make a delete account function