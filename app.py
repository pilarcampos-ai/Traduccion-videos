import streamlit as st
import yt_dlp
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

st.set_page_config(page_title="Traductor Pro", layout="centered")
st.title("🎬 Traductor de YouTube (Versión Estable)")

url = st.text_input("Pega el link de YouTube:")

if st.button("Traducir"):
    if url:
        with st.spinner("Conectando con YouTube..."):
            try:
                # CONFIGURACIÓN ANTI-BLOQUEO 403
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'audio_local.mp3',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'add_header': [
                        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language: en-US,en;q=0.5',
                    ],
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                st.write("Interpretando audio...")
                model = whisper.load_model("tiny")
                result = model.transcribe("audio_local.mp3", language="es")

                st.subheader("Traducción:")
                for segment in result['segments']:
                    st.markdown(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")

                if os.path.exists("audio_local.mp3"):
                    os.remove("audio_local.mp3")

            except Exception as e:
                st.error(f"Error detectado: {e}")
                st.info("Nota: Si el error 403 persiste, intenta con un video más corto o espera unos minutos.")
    else:
        st.warning("Introduce un link.")
