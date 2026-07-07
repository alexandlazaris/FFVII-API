from pydantic import BaseModel, Field, EmailStr

class Signup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)