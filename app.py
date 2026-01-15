import streamlit as st
import yt_dlp
import math
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Traductor YouTube", layout="centered")

st.title("Traductor YouTube → Español neutro")

url = st.text_input("Pegar link de YouTube")
