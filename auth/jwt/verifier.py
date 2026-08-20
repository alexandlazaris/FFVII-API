import os
import jwt
from jwt import PyJWKClient
from auth.jwt.principal import AuthenticatedUser
from auth.jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")

_jwks_client = PyJWKClient(
    f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
)

def verify_access_token(token: str) -> AuthenticatedUser:
    """
    Verify a Supabase access token.

    Raises:
        InvalidTokenError
        ExpiredTokenError

    Returns:
        AuthenticatedUser
    """
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
        )

        return AuthenticatedUser(
            user_id=claims["sub"],
            email=claims.get("email"),
        )

    except Exception as e:
        raise InvalidTokenError("Invalid or expired access token") from e