from typing import Optional
from pydantic import BaseModel

from models.common import CommonModel


class Product(CommonModel):
    name: str
    description: str


class UpdateProduct(BaseModel):
    name: Optional[str]
    description: Optional[str]
