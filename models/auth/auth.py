from pydantic import BaseModel, Field, EmailStr

class EmailPasswordCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class SignupRequest(EmailPasswordCredentials):
    pass

class LoginRequest(EmailPasswordCredentials):
    pass

class SignUpResponse(BaseModel):
    email: str
    email_verified: bool

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str