import streamlit as st
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

st.set_page_config(page_title="Traductor de Archivos", layout="centered")
st.title("🎬 Traductor de Video/Audio a Español")
st.write("Sube tu archivo para evitar los bloqueos de YouTube.")

# Componente para subir archivos
uploaded_file = st.file_uploader("Elige un archivo de video o audio (mp4, mp3, m4a, wav)", type=["mp4", "mp3", "m4a", "wav"])

if uploaded_file is not None:
    if st.button("Traducir archivo"):
        with st.spinner("Procesando archivo... Esto puede tardar unos minutos."):
            try:
                # Guardar el archivo temporalmente
                with open("temp_file", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Cargar IA Whisper
                model = whisper.load_model("tiny")
                
                # Transcribir y traducir
                result = model.transcribe("temp_file", language="es")

                st.subheader("Resultado minuto a minuto:")
                for segment in result['segments']:
                    st.write(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")

                # Limpiar
                os.remove("temp_file")

            except Exception as e:
                st.error(f"Error: {e}")
