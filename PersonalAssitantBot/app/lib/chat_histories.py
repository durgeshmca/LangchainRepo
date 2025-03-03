import psycopg
from langchain_postgres.chat_message_histories import PostgresChatMessageHistory
from app.config import Config

# create a store for session histories
# connection string to connect psycopg
class PostgresChatMessageHistoryStore:
    def __init__(self):
        pass
    def get_session_history(session_id):
        chat_history = PostgresChatMessageHistory(
            Config.CHAT_HISTORY_TABLE_NAME,
            session_id,
            sync_connection=psycopg.connect(Config.PG1_CONNECTION)
        )
        return chat_history
