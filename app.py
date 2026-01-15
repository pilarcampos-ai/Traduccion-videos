import streamlit as st
from pytube import YouTube
import whisper
import os

def format_time(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    else:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"minuto {minutes}:{remaining_seconds:02d}"

st.set_page_config(page_title="Traductor Sin Bloqueos", layout="centered")
st.title("🎬 Traductor de YouTube (Motor Pytube)")

url = st.text_input("Pega el link de YouTube:")

if st.button("Traducir"):
    if url:
        with st.spinner("Descargando audio (esto evita el error 403)..."):
            try:
                # 1. Descarga con Pytube
                yt = YouTube(url)
                # Seleccionamos solo el audio para que sea rápido
                audio_stream = yt.streams.filter(only_audio=True).first()
                archivo_descargado = audio_stream.download(filename="audio_temp.mp4")

                st.write("Interpretando y traduciendo a español neutro...")
                
                # 2. IA Whisper
                model = whisper.load_model("tiny")
                result = model.transcribe(archivo_descargado, language="es")

                st.subheader("Resultado:")
                for segment in result['segments']:
                    st.write(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")

                # Limpieza
                if os.path.exists(archivo_descargado):
                    os.remove(archivo_descargado)

            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Si el error persiste, YouTube ha bloqueado la IP de este servidor. Prueba borrar la App en Streamlit Cloud y crearla de nuevo para cambiar de IP.")
    else:
        st.warning("Introduce un link.")
