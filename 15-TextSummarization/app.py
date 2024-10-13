import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

# Streamlit app
st.set_page_config("Summarize Text from youtube or any website",page_icon="🦜")
st.title("Summarize text from you tube or from any website.")
st.subheader("Summarize URL")

# Get Groq Key and url field
with st.sidebar:
    groq_api_key = st.text_input("Enter Groq API Key",type="password")


web_url = st.text_input("URL",label_visibility="collapsed")

#  Model

llm = ChatGroq(model="gemma2-9b-it",api_key=groq_api_key)
prompt_template = """
Provide a summary of the following content in 300 words
Content : {text}
"""
prompt = PromptTemplate(template=prompt_template,input_variables=['text'])


################################

if st.button("Summarize the content"):
    if not groq_api_key.strip() and web_url.strip():
        st.error("Please enter required fields")
    elif not validators.url(web_url):
        st.error("Invalid URL provided")
    else:
        try:
            with st.spinner("Waiting.."):
                # loading data from web
                if "youtube.com" in web_url:
                    video_id = web_url.split("=")[1]
                    loader = YoutubeLoader(video_id,add_video_info=True)
                else:
                    loader = UnstructuredURLLoader([web_url],
                                                   ssl_verify=False,
                                                   headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
                                                   )
                docs = loader.load()
                # Enhancement first check if the content fits  to llm context window
                # If fites then use stuff summarization otherwise use map_reduce
                # chain summaization
                chain = load_summarize_chain(
                    llm,
                    chain_type="stuff",
                    prompt=prompt
                )
                output_summary = chain.invoke(docs)
                st.success(output_summary['output_text'])
        except Exception as e:
            st.exception(e)
            
        
