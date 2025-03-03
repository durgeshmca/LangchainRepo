from pydantic import BaseModel

class Chat(BaseModel):
    session_id : str
    message : str

