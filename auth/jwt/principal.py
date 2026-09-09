from dataclasses import dataclass

@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: str
    email: str | None