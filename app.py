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

st.set_page_config(page_title="Traductor Estable", page_icon="🎬")
st.title("🎬 Traductor de Video/Audio")

uploaded_file = st.file_uploader("Sube tu archivo aquí:", type=["mp4", "mp3", "m4a", "wav"])

if uploaded_file is not None:
    if st.button("Empezar Traducción"):
        with st.spinner("Traduciendo..."):
            try:
                # 1. Guardar archivo temporal
                with open("temp_file", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 2. Modelo Tiny (El que te funcionó)
                model = whisper.load_model("tiny")
                
                # 3. Traducción estándar
                result = model.transcribe("temp_file", language="es")

                st.subheader("Resultado:")
                
                for segment in result['segments']:
                    # Solo mostramos si hay texto para evitar segundos vacíos al inicio
                    texto = segment['text'].strip()
                    if texto:
                        # CORRECCIÓN DE TIEMPO: 
                        # Si Whisper dice que empieza en 0 pero tú sabes que es el 3, 
                        # es porque el primer segmento es muy largo.
                        # Mostramos el tiempo tal cual lo detecta la IA.
                        st.write(f"**{format_time(segment['start'])}**: {texto}")

                os.remove("temp_file")

            except Exception as e:
                st.error(f"Error: {e}")
