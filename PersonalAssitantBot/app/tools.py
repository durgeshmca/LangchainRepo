from app.lib.doc_tools import document_retriver_tool
from langchain_community.tools import TavilySearchResults

search_tool = TavilySearchResults(k=6)

tools = [search_tool, document_retriver_tool]

