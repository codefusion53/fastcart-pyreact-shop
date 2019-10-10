from typing import Union, Optional
from pydantic import BaseModel

from models.common import CommonModel


class User(CommonModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
