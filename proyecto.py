import streamlit as st
from langchain_openai import ChatOpenAI
from modulos.busqueda_tavily import lookup
from modulos.obt_titulo import obtener_titulo
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

if prompt := st.chat_input("Ingresa tu tema de investigacion"):
    user_mg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_mg)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        #message_placeholder = st.empty()
        with st.spinner("Pensando..."):
            searched_info = lookup(prompt, llm)
            
            all_contents = "\n\n".join([item['content'] for item in searched_info])
            summary_prompt = HumanMessage(content=f"Resume la siguiente información:\n\n{all_contents}")
            response = llm([summary_prompt])
            
        st.markdown("### Resumen")    
        st.markdown(response.content)
        st.markdown("### Fuentes de información")
        
        for item in searched_info:
            title = obtener_titulo(item["url"])
            st.markdown(f"#### {title}")
            st.markdown(f"[{item['url']}]({item['url']})")
            snippet = item['content'][:300] + "..." if len(item['content']) > 350 else item['content']
            st.markdown(f"> {snippet}")
            st.markdown("---")
        
        # Generate WordCloud
        st.markdown("### Nube de Palabras")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_contents)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    st.session_state.messages.append(response)