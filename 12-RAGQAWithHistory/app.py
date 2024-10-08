import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os

from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = "Chat-QA-with-history"
llm = ChatGroq(model='llama3-8b-8192')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')

if "store" not in st.session_state:
    st.session_state.store = {}


def get_session_history(session_id:str)->BaseChatMessageHistory:
        if session_id not in st.session_state.store:
            st.session_state.store[session_id]=ChatMessageHistory()
        return st.session_state.store[session_id]

st.title("Question answer chatbot with History")
session_id = st.text_input("Session ID:",value="default_session")
uploaded_files = st.file_uploader("Upload PDF file to query",accept_multiple_files=False,type=["pdf"])
# uploaded_files.getvalue
if uploaded_files:
    temp_pdf = './tmppdf.pdf'
    with open(temp_pdf, 'wb') as f:
        f.write(uploaded_files.getvalue())
        print("File saved")
    # load pdf as Document and create embedding and vectorstore
    docs = PyPDFLoader(temp_pdf).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vectorstore = Chroma.from_documents(docs,embedding)
    st.write("Vector store created successfully")
    
    retriever = vectorstore.as_retriever()

    # conceptualize message prompt
    contextualize_q_system_prompt_template=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ('system',contextualize_q_system_prompt_template),
            MessagesPlaceholder("chat_history"),
            ('human',"{input}")
        ]
    )
    history_aware_retriever = create_history_aware_retriever(llm,retriever,contextualize_q_prompt)

    ## Answer question

        # Answer question
    system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
    qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
    qa_doc_chain = create_stuff_documents_chain(llm,qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever,qa_doc_chain)

    conversational_rag_chain=RunnableWithMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )


    

    input = st.text_input("Ask any question based on uploaded document")
    if input :
          session_history = get_session_history(session_id)
          response = conversational_rag_chain.invoke(
                {"input": input},
                config={
                    "configurable": {"session_id":session_id}
                },  # constructs a key "abc123" in `store`.
            )
          st.write("Assistant",response['answer'])
          st.write("store",st.session_state.store)
          st.write("chat_history",session_history.messages)
        
    



    
        
    
