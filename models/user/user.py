from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class GetUserResponse(BaseModel):
    user_id: str
    email: Optional[EmailStr] = None
    is_anonymous: bool
    last_sign_in_at: Optional[datetime] = None