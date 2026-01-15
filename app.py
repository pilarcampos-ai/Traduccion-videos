import streamlit as st
import whisper
import os

def format_time(seconds):
    seconds = int(seconds)
    if seconds < 60: return f"segundo {seconds}"
    return f"minuto {seconds // 60}:{seconds % 60:02d}"

st.set_page_config(page_title="Traductor Total", page_icon="🎬")
st.title("🎬 Traductor de Video o Subtítulos")

# Opción para elegir qué subir
opcion = st.radio("¿Qué vas a subir?", ["Video/Audio (Para que la IA escuche)", "Archivo SRT (Subtítulos en inglés)"])

if opcion == "Video/Audio (Para que la IA escuche)":
    uploaded_file = st.file_uploader("Sube tu video o audio:", type=["mp4", "mp3", "m4a", "wav"])
    if uploaded_file and st.button("Traducir Audio"):
        with st.spinner("Escuchando..."):
            with open("temp", "wb") as f: f.write(uploaded_file.getbuffer())
            model = whisper.load_model("tiny")
            result = model.transcribe("temp", language="es")
            for segment in result['segments']:
                st.write(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")
            os.remove("temp")

else:
    srt_file = st.file_uploader("Sube tu archivo .srt en inglés:", type=["srt"])
    if srt_file and st.button("Traducir Subtítulos"):
        st.write("### Traducción de Subtítulos:")
        lineas = srt_file.getvalue().decode("utf-8").splitlines()
        for linea in lineas:
            # Este bloque identifica tiempos y texto en el archivo SRT
            if "-->" in linea:
                tiempo_seg = linea.split(":")[1] # Extrae el minuto/segundo básico
                st.write(f"**Tiempo: {linea.split(',')[0]}**")
            elif linea.strip() and not linea.strip().isdigit():
                # Aquí podrías conectar una API de traducción o simplemente 
                # mostrar el texto para traducir.
                st.write(f"Traducción: {linea}")
