import streamlit as st
import yt_dlp
import math
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Traductor YouTube", layout="centered")

# LOGIN SIMPLE
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("Login equipo")

    user = st.text_input("Usuario")
    pwd = st.text_input("Password", type="password")

    if st.button("Ingresar"):
        if user == "equipo" and pwd == "password123":
            st.session_state.logged = True
        else:
            st.error("Credenciales incorrectas")
    st.stop()

st.title("Traductor YouTube → Español")

url = st.text_input("Pegar link de YouTube")

def extract_subs(url):
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        subs = info.get("subtitles") or info.get("automatic_captions")
        captions = subs["en"][0]["data"]

    return [(math.floor(c["start"]), c["text"].replace("\n", " ")) for c in captions]

def translate(text):
    r = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Traduce al español neutro, tono tutorial, natural."},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return r.choices[0].message.content.strip()

def fmt(sec):
    if sec < 60:
        return f"segundo {sec}"
    return f"minuto {sec//60}:{str(sec%60).zfill(2)}"

if st.button("Procesar") and url:
    with st.spinner("Procesando..."):
        subs = extract_subs(url)
        out = []
        for s, t in subs:
            if t.strip():
                out.append(f"{fmt(s)}: {translate(t)}")
        st.text_area("Resultado", "\n".join(out), height=400)
