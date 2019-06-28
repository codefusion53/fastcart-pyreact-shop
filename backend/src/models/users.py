from typing import Optional
from pydantic import BaseModel, EmailStr

from models.common import CommonModel


class User(CommonModel):
    email: EmailStr


class UpdateUser(BaseModel):
    email: Optional[EmailStr]
