from app.lib.doc_tools import document_retriver_tool
from app.lib.chat_tools import chat_retriever_tool
from app.config import Config
from langchain_community.tools import TavilySearchResults
search_tool = TavilySearchResults(k=3,tavily_api_key=Config.TAVILY_API_KEY)

tools = [search_tool, document_retriver_tool,chat_retriever_tool]

