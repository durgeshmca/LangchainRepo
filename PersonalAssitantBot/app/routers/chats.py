from fastapi import APIRouter,Body,Depends
from app.models.users import UserBase
from app.models.chat import Chat
from app.lib.agents import agent_with_history
from typing import Annotated
from app.auth import get_current_active_user


chat_router = APIRouter()
@chat_router.post("/chat",tags=["chat"])
async def chat_message( 
    current_user: Annotated[UserBase, Depends(get_current_active_user)],
    chat: Annotated[Chat, Body()]
    ):
        response = response = agent_with_history.invoke(
            {"input": chat.message},
            config={"configurable": {"session_id": str(current_user.user_uuid)}},
        )
        return response
# @users_router.post("/users",response_model=UserBase,tags=["users"])
# async def create_new_user(user: Annotated[UserCreate, Body()],
#                           session:SessionDep):
#    user.password = get_password_hash(user.password)
#    user = create_user(session, user)
#    return user

# @users_router.get("/users/me/", 
#             response_model=UserBase,
#             tags=["users"]
#         )
# async def read_users_me(
#     current_user: Annotated[UserBase, Depends(get_current_active_user)],
# ):
#     return current_user



