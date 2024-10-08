from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import os,time
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model='gemma-7b-it')

template = '''
    Answer the question based on the provided context only.
    Provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Question: {input}                                      
'''
prompt = ChatPromptTemplate.from_template(template)
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')

def create_vector_embedding():
    if "vectorstore" not in st.session_state:

        st.session_state.embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        st.session_state.loader = PyPDFDirectoryLoader('research_papers')
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.spliter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
        st.session_state.final_docs = st.session_state.spliter.split_documents(st.session_state.docs)
        st.session_state.vectorstore = FAISS.from_documents(st.session_state.final_docs,st.session_state.embedding)

question = st.text_input("Ask any question from the research paper.")
if st.button("Document Embeddings"):
    create_vector_embedding()
    st.write("Vector DB cretaed")


if question:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriver = st.session_state.vectorstore.as_retriever()
    retriver_chain = create_retrieval_chain(retriever=retriver,combine_docs_chain=document_chain)
    start = time.process_time()
    response = retriver_chain.invoke({'input':question})['answer']
    st.write(f"Response Time: {time.process_time() - start}")
    st.write(response)

