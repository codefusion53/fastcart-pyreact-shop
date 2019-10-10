from typing import List
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson.errors import InvalidId

from database import db
from models.users import User, UpdateUser
from auth.utils import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def parse_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")


@router.get("/", response_model=List[User])
async def get_users():
    users = await db["users"].find().to_list(100)
    return users


@router.get("/{id}", response_model=User)
async def get_user(id: str):
    oid = parse_object_id(id)
    if (user := await db["users"].find_one({"_id": oid})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User = Body(...), current_user: dict = Depends(get_current_user)):
    user = jsonable_encoder(user)
    user.pop("_id", None)
    now = datetime.utcnow()
    user["created_at"] = now
    user["updated_at"] = now
    result = await db["users"].insert_one(user)
    created = await db["users"].find_one({"_id": result.inserted_id})
    return created


@router.put("/{id}", response_model=User)
async def update_user(id: str, user: UpdateUser = Body(...), current_user: dict = Depends(get_current_user)):
    oid = parse_object_id(id)
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        result = await db["users"].update_one({"_id": oid}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    if (existing := await db["users"].find_one({"_id": oid})) is not None:
        return existing
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, current_user: dict = Depends(get_current_user)):
    oid = parse_object_id(id)
    result = await db["users"].delete_one({"_id": oid})
    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User {id} not found")
