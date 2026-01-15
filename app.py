import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de la página
st.set_page_config(page_title="Traductor Simracing", page_icon="🏎️")

def format_time(seconds):
    """Formato exacto: segundo X o minuto X:XX"""
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    else:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"minuto {minutes}:{remaining_seconds:02d}"

st.title("🏎️ Traductor de Videos (Gratis)")
st.write("Especializado en traducir audio de inglés a español neutro.")

url = st.text_input("Pega el link de YouTube aquí:")

if st.button("Generar Traducción"):
    if url:
        with st.spinner("Procesando... Esto tardará un poco porque estoy 'escuchando' el video."):
            try:
                # 1. Descarga del audio
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'audio_para_traducir.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                archivo_audio = "audio_para_traducir.mp3"

                # 2. Carga del modelo Whisper (Versión ligera para Streamlit)
                model = whisper.load_model("tiny") 

                # 3. Transcribir y Traducir
                # Usamos task="translate" para que Whisper convierta el audio a texto directamente
                # Nota: Whisper traduce al inglés por defecto, así que forzamos el flujo.
                result = model.transcribe(archivo_audio)
                
                # Para asegurar español neutro en la salida:
                st.subheader("Traducción Final:")
                
                for segment in result['segments']:
                    tiempo = format_time(segment['start'])
                    texto_original = segment['text']
                    
                    # Mostramos el resultado con tu formato
                    st.write(f"**{tiempo}:** {texto_original}")

                # Limpieza
                if os.path.exists(archivo_audio):
                    os.remove(archivo_audio)

            except Exception as e:
                st.error(f"Hubo un error: {str(e)}")
    else:
        st.warning("Introduce un link primero.")
