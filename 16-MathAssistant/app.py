import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

## Set upi the Stramlit app
st.set_page_config(page_title="Text To MAth Problem Solver And Data Serach Assistant",page_icon="🧮")
st.title("Text To Math Problem Solver Uing Google Gemma 2")

groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")


if not groq_api_key:
    st.info("Please add your Groq APPI key to continue")
    st.stop()

llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1)
wikipedia_tool = Tool(
    name="WekipediaSearch",
    func= wikipedia_wrapper.run,
    description= "Tool for searching the internet to find the various information on the topic mentioned"
)

# initialize the math tool
match_chain = LLMMathChain.from_llm(llm)
calculator = Tool(
    name="Calculator",
    func= match_chain.run,
    description="Answers math related questions and accepts only mathematical expressions"
)

prompt = """You are an agent to solve mathematical question.
Logically arrive at solution of the given problem and display it point wise for the question below.
Question: {question}
Answer:
"""
prompt_template = PromptTemplate(input_variables=['question'],template=prompt)

# combine all the tools into chain
chain = LLMChain(
    llm=llm,
    prompt= prompt_template,

)

reasoning_tool = Tool(
    name="reasoning",
    func= chain.run,
    description="A tool for answering logical and reasoning questions"

)

# Initialize the agent
agent = initialize_agent(
    tools=[wikipedia_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_erros=True
)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role":"assistant","content":"Hi ,I am your math assistant. You can ask any math related questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


# function to generate response
def generate_response(question:str):
    response = agent.invoke(input={'question':question})
    return response

question = st.text_area("Enter your question: ","Find the cost of fencing a square field of 175m at Rs.60 per metre")

if st.button("Submit the question")  :
   if question:
       with st.spinner('Generating response') :
           st.session_state.messages.append({"role":"user","content":question})
           st.chat_message("user").write(question)
           st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=True)
           response = agent.run(st.session_state.messages,callbacks=[st_cb])
           st.session_state.messages.append({'role':'assistant',"content":response})
           st.write('### Response:')
           st.success(response)
   else:
       st.warning("enter the question please")
           
#    response = generate_response(question)
   