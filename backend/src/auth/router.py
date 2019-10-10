from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status

from auth.models import Token, UserLoginSchema, UserSignupSchema
from auth.utils import hash_password, verify_password, create_access_token, get_current_user
from database import db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(user: UserSignupSchema = Body(...)):
    if await db["users"].find_one({"email": user.email}) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    if user.password != user.password_confirmation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    new_user = {
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db["users"].insert_one(new_user)
    created = await db["users"].find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    created.pop("hashed_password", None)
    return created


@router.post("/login", response_model=Token)
async def login(user: UserLoginSchema = Body(...)):
    registered = await db["users"].find_one({"email": user.email})
    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if registered is None or not verify_password(user.password, registered.get("hashed_password", "")):
        raise invalid

    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
