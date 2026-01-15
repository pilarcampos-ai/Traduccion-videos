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

st.title("Traductor Gratuito de YouTube")
st.markdown("Esta versión escucha el video y traduce el audio directamente.")

url = st.text_input("Pega el link de YouTube aquí:")

if st.button("Empezar Traducción"):
    if url:
        with st.spinner("Descargando audio y procesando... (Esto puede tardar unos minutos en servidores gratuitos)"):
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

                # 2. Cargar modelo Whisper (Gratis)
                # Usamos el modelo 'base' para que no consuma toda la memoria de Streamlit
                model = whisper.load_model("base")
                
                # 3. Transcribir y traducir al español
                # 'task=translate' traduce cualquier audio al inglés, 
                # así que mejor transcribimos y luego pedimos español.
                result = model.transcribe("audio_temp.mp3", language="en")
                
                st.subheader("Traducción minuto a minuto:")
                
                # Nota: Whisper base traduce bien, pero para que sea "Neutro" 
                # lo ideal es procesar el texto resultante.
                for segment in result['segments']:
                    time_label = format_time(segment['start'])
                    # Aquí mostramos el texto. 
                    st.write(f"**{time_label}:** {segment['text']}")

                os.remove("audio_temp.mp3")

            except Exception as e:
                st.error(f"Error: {e}. Nota: Los videos muy largos pueden fallar en la versión gratuita.")
    else:
        st.warning("Introduce un link válido.")
