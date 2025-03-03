# Implementing PDF Search
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools.retriever import create_retriever_tool
from enum import Enum
from app.config import Config

class DocType(Enum):
    pdf  = "pdf"
    docx = "docx"
    web  = "web_url"


class VectoreStore:
    def __init__(self, connection:str, collection_name:str,embeddings):
        self.vectorestore = PGVector(
            embeddings=embeddings,
            connection=connection,
            collection_name=collection_name,
            use_jsonb=True,
        )

    # add pdf to store
    def add_doc_to_store(self,doc_type:DocType,doc_location="data/What_Is_AI.pdf"):
        try :
            if doc_type == DocType.pdf:
                loader = PyPDFLoader(doc_location)
            # pdf_loader = PyPDFLoader(doc_location)
            # text splitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            # split the document
            split_docs = loader.load_and_split(text_splitter=text_splitter)
            self.vectorestore.add_documents(split_docs)
        except Exception as e:
            raise Exception(f"Error adding document to store: {e}")
        
    def get_retriver_tool(self):
        retriver = self.vectorestore.as_retriever()
        # create retriver tool
        retriver_tool = create_retriever_tool(
            retriever=retriver,
            name="document_search",
            description="Use this tool to search information from the pdf document"
        )
        return retriver_tool
# create vectore store
vectore_store = VectoreStore(
    connection=Config.PG_CONNECTION,
    collection_name=Config.PG_COLLECTION_NAME,
    embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
)

document_retriver_tool = vectore_store.get_retriver_tool()
