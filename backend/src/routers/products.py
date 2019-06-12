from typing import List
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from database import db
from models.products import Product, ProductUpdate


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[Product])
async def get_products():
    products = await db["products"].find().to_list(100)
    return products


@router.get("/{id}", response_model=Product)
async def get_product(id: str):
    if (product := await db["products"].find_one({"_id": id})) is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product = Body(...)):
    product = jsonable_encoder(product)
    now = datetime.utcnow()
    product["created_at"] = now
    product["updated_at"] = now
    result = await db["products"].insert_one(product)
    created = await db["products"].find_one({"_id": result.inserted_id})
    return created


@router.put("/{id}", response_model=Product)
async def update_product(id: str, product: ProductUpdate = Body(...)):
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        result = await db["products"].update_one({"_id": id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

    if (existing := await db["products"].find_one({"_id": id})) is not None:
        return existing
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    result = await db["products"].delete_one({"_id": id})
    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
