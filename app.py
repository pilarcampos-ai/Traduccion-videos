import streamlit as st
import yt_dlp
import os
from openai import OpenAI

# Configura tu clave de API de OpenAI
# Recomiendo ponerla en los "Secrets" de Streamlit para mayor seguridad
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def format_time(seconds):
    """Convierte segundos al formato 'segundo X' o 'minuto X:XX'"""
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    else:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"minuto {minutes}:{remaining_seconds:02d}"

st.title("Traductor de Videos Pro (Inglés a Español)")

url = st.text_input("Pega el link de YouTube aquí:")

if st.button("Traducir Video"):
    if url:
        with st.spinner("Extrayendo audio y traduciendo... esto puede tardar un minuto."):
            try:
                # 1. Descargar Audio
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'audio_temp.mp3',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 2. Traducir con OpenAI Whisper
                audio_file = open("audio_temp.mp3", "rb")
                # La tarea 'translate' traduce automáticamente cualquier idioma al inglés.
                # Para español neutro, pediremos una transcripción y luego una traducción.
                transcript = client.audio.translations.create(
                    model="whisper-1", 
                    file=audio_file,
                    response_format="verbose_json"
                )

                # 3. Mostrar resultados con TU formato
                st.subheader("Resultado de la traducción:")
                for segment in transcript.segments:
                    time_label = format_time(segment['start'])
                    texto = segment['text']
                    st.write(f"**{time_label}:** {texto}")
                
                # Limpiar archivo temporal
                os.remove("audio_temp.mp3")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor, introduce un link.")

