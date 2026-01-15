import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de formato de tiempo
def format_time(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    else:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"minuto {minutes}:{remaining_seconds:02d}"

st.set_page_config(page_title="Traductor de Videos Pro", layout="centered")
st.title("🎬 Traductor de YouTube Gratis")
st.write("Traducción a español neutro sin usar APIs de pago.")

url = st.text_input("Pega el link de YouTube:")

if st.button("Traducir"):
    if url:
        with st.spinner("1. Descargando audio del video..."):
            try:
                # Opciones para descargar audio sin bloqueos
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'audio_local.mp3',
                    'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}],
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                st.write("2. Escuchando y traduciendo (IA)...")
                # Cargamos el modelo más ligero para que la App no se cuelgue
                model = whisper.load_model("tiny")
                
                # Traducimos directamente
                result = model.transcribe("audio_local.mp3", language="es")

                st.subheader("Traducción Terminada:")
                for segment in result['segments']:
                    # Formato minuto a minuto que pediste
                    st.markdown(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")

                # Borrar archivo temporal
                os.remove("audio_local.mp3")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Introduce un link válido.")
