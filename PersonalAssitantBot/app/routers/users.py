from fastapi import APIRouter
from app.models.users import UserBase
from app.auth import (
    Annotated,
    Depends,
    get_current_active_user
)

users_router = APIRouter()

@users_router.get("/users/me/", 
            response_model=UserBase,
            tags=["users"]
        )
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
):
    return current_user

@users_router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@users_router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

