from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate,
)

llm = ChatOllama(model="llama2") 

st.title("Code Generator ")
st.caption("Your AI pair Programmer With Debugging Super Power")
# Sidebar configuration 
with st.sidebar:
    st.header("Model Configuration")
    selected_model = st.selectbox(
        "Choose MOdel",
        ["Deepseek-r1:1.5b","Add model"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities ")
    st.markdown("""
                Python Expert\n
                Debugging Assistant\n
                Code Documentation\n
                Solution Design
                """)
    st.divider()
    st.markdown("Built with [Ollama](https:/ollama.ai/) || [Langchain](https://python.langchain.com/)")
    st.header("Devloper Name :- Banvaree Lal Dangi")
    #####################
def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | lim_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)
    ##############################

    # initiate the chat engine
lim_engine = ChatOllama(model=selected_model,
                        base_url="http://localhost:11434",
                        temperature=0.3)
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide concise, correct solution"
    "with strategic print statement for debogging . Always respond in English"
)

    # Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log =[{"role":"ai", "content":"Hi ! I'm Python, How can I help you today ?"}]
    
    # Chat container
chat_container = st.container()

    # Display Chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
user_query = st.chat_input("Type your coding question here ...")
if user_query:
    st.session_state.message_log.append({"role":"user", "content":user_query})

        # Generate AI response
    with st.spinner(" Processing.... Thinking please wait... "):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(build_prompt_chain())

        # Add AI response to log 
    st.session_state.message_log.append({"role":"ai", "content": ai_response})

        # Return to update chat display
    st.rerun()