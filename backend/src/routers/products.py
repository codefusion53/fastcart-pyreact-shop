from typing import List
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson.errors import InvalidId

from database import db
from models.products import Product, UpdateProduct


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


def parse_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")


@router.get("/", response_model=List[Product])
async def get_products():
    products = await db["products"].find().to_list(100)
    return products


@router.get("/{id}", response_model=Product)
async def get_product(id: str):
    oid = parse_object_id(id)
    if (product := await db["products"].find_one({"_id": oid})) is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product = Body(...)):
    product = jsonable_encoder(product)
    # Let MongoDB assign a native ObjectId rather than storing a stringified one.
    product.pop("_id", None)
    now = datetime.utcnow()
    product["created_at"] = now
    product["updated_at"] = now
    result = await db["products"].insert_one(product)
    created = await db["products"].find_one({"_id": result.inserted_id})
    return created


@router.put("/{id}", response_model=Product)
async def update_product(id: str, product: UpdateProduct = Body(...)):
    oid = parse_object_id(id)
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        result = await db["products"].update_one({"_id": oid}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

    if (existing := await db["products"].find_one({"_id": oid})) is not None:
        return existing
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    oid = parse_object_id(id)
    result = await db["products"].delete_one({"_id": oid})
    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
