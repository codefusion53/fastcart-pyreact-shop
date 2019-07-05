from typing import Optional
from pydantic import BaseModel

from models.common import CommonModel


class Product(CommonModel):
    name: str
    description: str
    price: Optional[float] = 0.00


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
