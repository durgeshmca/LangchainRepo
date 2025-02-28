from fastapi import FastAPI
from app.routers.auth import  auth_router
from app.routers.users import users_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
