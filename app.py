import streamlit as st
import yt_dlp
import math
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Traductor YouTube", layout="centered")

st.title("Traductor YouTube → Español neutro")

url = st.text_input("Pegar link de YouTube")

if st.button("Procesar video"):
    if not url:
        st.error("Por favor, pegá un link de YouTube")
    else:
        try:
            st.info("Procesando video... esto puede tardar unos segundos")
            # acá sigue tu lógica actual
        except Exception as e:
            st.error(f"Error: {e}")

