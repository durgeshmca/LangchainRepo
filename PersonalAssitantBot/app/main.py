from fastapi import FastAPI
from app.routers.auth import  auth_router
from app.routers.users import users_router
from app.routers.chats import chat_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)
