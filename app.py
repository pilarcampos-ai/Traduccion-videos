import streamlit as st
import whisper
import gdown
import os
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Traductor de Voz en Off")

st.title("🎙️ Traductor de Audio (Whisper AI)")
st.write("Escucha el audio del video de Drive y lo traduce al español.")

drive_url = st.text_input("Pegá el link de Google Drive (Público):")

if drive_url and st.button("Procesar Audio"):
    status = st.empty()
    try:
        output = "video_audio.mp4"
        status.info("Descargando video de Drive...")
        gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
        
        # Usamos el modelo 'tiny' que es el más liviano para que no se caiga el servidor
        status.info("Cargando IA de voz (Whisper Tiny)...")
        model = whisper.load_model("tiny")
        
        status.info("Escuchando y traduciendo...")
        resultado = model.transcribe(output)
        translator = GoogleTranslator(source='en', target='es')
        
        st.subheader("Traducción del audio:")
        for segment in resultado['segments']:
            inicio = int(segment['start'])
            traduccion = translator.translate(segment['text'])
            tiempo = f"{inicio // 60:02d}:{inicio % 60:02d}"
            st.write(f"**[{tiempo}]**: {traduccion}")
            
        os.remove(output)
        status.success("¡Completado!")
        
    except Exception as e:
        st.error(f"Error: {e}")
