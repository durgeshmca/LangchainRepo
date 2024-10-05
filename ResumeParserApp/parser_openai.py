import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')

def get_pdf_data(pdf_doc):
    text = ""
    # for pdf in pdf_docs:
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
# create chat prompt 
prompt = ChatPromptTemplate.from_messages(
    [
    ('system','You are an expert resume parser. Parse the resume given and respond in json format. Outpout must be grouped under following categories:\
     personal information,experience,skills,education,interpersonal_skills and others.'),
    ('user','Resume : {resume}')
    ]
)
# call Ollama llama3 model
llm = ChatOpenAI()

#output parser
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

## streamlt framework
st.set_page_config("ResumeParser")
st.header("Resume Parser Support💁")
st.title("Resume Parser App")
resume_file = st.file_uploader('Please upload your resume')
input_url = st.text_input('Please enter linkedin url')

if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_data(resume_file)
                st.write(chain.invoke({'resume': raw_text}))
                st.success("Done")
if input_url:
    with st.spinner("Processing..."):
                raw_text = get_pdf_data(resume_file)
                st.write(chain.invoke({'resume': raw_text}))
                st.success("Done")
    # st.write(chain.invoke({'question': input_text}))



# if input_text:
#     st.write(chain.invoke({'question': input_text}))


