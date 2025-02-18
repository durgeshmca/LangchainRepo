import streamlit as st
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')
docs = PyPDFDirectoryLoader('uploads').load()
print("Documents uploaded",len(docs))
splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
split_docs = splitter.split_documents(docs)
embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vectorstore = Chroma.from_documents(split_docs,embedding,persist_directory="./chroma_db")

st.title("Research Paper Management")
uploaded_files = st.file_uploader("Upload PDF file of research paper",accept_multiple_files=False,type=["pdf"])
if uploaded_files:
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    temp_pdf = 'uploads/tmppdf_'+str(current_datetime)+'pdf'
    with open(temp_pdf, 'wb') as f:
        f.write(uploaded_files.getvalue())
        print("File saved")
    # load pdf as Document and create embedding and vectorstore
    docs = PyPDFLoader(temp_pdf).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vectorstore=Chroma(persist_directory='./chroma_db',embedding_function=embedding)
    vectorstore.add_documents(docs)
    st.write("PDF Added to vectore store")
    
    retriever = vectorstore.as_retriever()

   

    input = st.text_input("Ask any question based on uploaded documents")
    if input :
          response = retriever.invoke(input)
          for result in response:
               st.write("Search Result:",result.page_content)
               st.write(result.metadata)
          
        
    



    
        
    
