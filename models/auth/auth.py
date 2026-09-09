from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class EmailPasswordCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class SignupRequest(EmailPasswordCredentials):
    pass

class LoginRequest(EmailPasswordCredentials):
    pass

class SignUpConfirmRequest(BaseModel):
    token_hash: str

class SignUpResponse(BaseModel):
    email: Optional[EmailStr] = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class LogoutResponse(BaseModel):
    result: str

class SignUpConfirmedResponse(BaseModel):
    id: str
    email: Optional[EmailStr] = None
    confirmed_at: Optional[datetime] = None