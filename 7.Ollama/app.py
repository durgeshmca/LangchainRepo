import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')

# create chat prompt 
prompt = ChatPromptTemplate.from_messages(
    [
    ('system','You are an helpful assistance .Answer the question asked'),
    ('user','Question: {question}')
    ]
)

## streamlt framework
st.title("Langchain demo with Gemma 2")
input_text = st.text_input('Ask a question')

# call Ollama llama3 model
llm = Ollama(model='llama3')

#output parser
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({'question': input_text}))
