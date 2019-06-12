from typing import List
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from database import db
from models.users import User, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[User])
async def get_users():
    users = await db["users"].find().to_list(100)
    return users


@router.get("/{id}", response_model=User)
async def get_user(id: str):
    if (user := await db["users"].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    now = datetime.utcnow()
    user["created_at"] = now
    user["updated_at"] = now
    result = await db["users"].insert_one(user)
    created = await db["users"].find_one({"_id": result.inserted_id})
    return created


@router.put("/{id}", response_model=User)
async def update_user(id: str, user: UserUpdate = Body(...)):
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        result = await db["users"].update_one({"_id": id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    if (existing := await db["users"].find_one({"_id": id})) is not None:
        return existing
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    result = await db["users"].delete_one({"_id": id})
    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User {id} not found")
