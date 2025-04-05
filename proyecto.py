import streamlit as st
from langchain_openai import ChatOpenAI
from modulos.busqueda_tavily import lookup
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature = 0, model_name = "gpt-4o-mini", openai_api_key = OPENAI_API_KEY)

st.title("Asistente de investigación digital")

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="Eres un asistente enfocado en la investigacion digital, debes de buscar información actualizada en la web, analizarla utilizando modelos de lenguaje y presentar un resumen junto con una visualización interactiva de las palabras más frecuentes.")]

for smg in st.session_state.messages[1:]:
    with st.chat_message("user" if isinstance(smg, HumanMessage) else "assistant"):
        st.markdown(smg.content)

if prompt := st.chat_input("Ingresa tu mensaje"):
    user_mg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_mg)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Pensando..."):
            searched_info = lookup(prompt, llm)
            response = llm(st.session_state.messages)
        message_placeholder.markdown(response.content)
        message_placeholder.markdown(searched_info)

    st.session_state.messages.append(response)
    st.session_state.messages.append(searched_info)