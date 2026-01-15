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

st.set_page_config(page_title="Traductor Sin Bloqueos", page_icon="🎬")
st.title("🎬 Traductor por Archivo (Sin Errores)")
st.write("Sube tu video o audio descargado para obtener la traducción minuto a minuto.")

# Aquí cambiamos el link por un cargador de archivos
uploaded_file = st.file_uploader("Sube tu video o audio aquí:", type=["mp4", "mp3", "m4a", "wav"])

if uploaded_file is not None:
    if st.button("Empezar Traducción"):
        with st.spinner("La IA está escuchando tu archivo... Esto tarda un par de minutos."):
            try:
                # Guardar el archivo subido de forma temporal
                with open("archivo_temp", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Cargamos la IA (Versión ligera para que no se cuelgue)
                model = whisper.load_model("tiny")
                
                # Traducir (Task translate lo pasa a inglés, pero forzamos español)
                result = model.transcribe("archivo_temp", language="es")

                st.success("¡Traducción completada!")
                st.subheader("Resultado:")
                
                for segment in result['segments']:
                    st.write(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")

                # Borramos el temporal para no llenar el servidor
                if os.path.exists("archivo_temp"):
                    os.remove("archivo_temp")

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
