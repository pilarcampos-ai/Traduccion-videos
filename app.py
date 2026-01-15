import streamlit as st
import whisper
import gdown
import os
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Traductor de Voz en Off")

st.title("🎙️ Traductor de Audio (Whisper AI)")
st.write("Ideal para videos con locución. Escucha el audio y lo traduce.")

drive_url = st.text_input("Pega el link de Google Drive (Público):")

if drive_url and st.button("Procesar Audio"):
    status = st.empty()
    try:
        # 1. Descarga
        output = "video_audio.mp4"
        status.info("Descargando video de Drive...")
        gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
        
        # 2. IA de Audio (Modelo Tiny para no saturar RAM)
        status.info("Cargando IA de voz (Whisper Tiny)...")
        model = whisper.load_model("tiny")
        
        # 3. Transcribir y Traducir
        status.info("Escuchando y traduciendo...")
        resultado = model.transcribe(output)
        translator = GoogleTranslator(source='en', target='es')
        
        st.subheader("Traducción del audio:")
        
        for segment in resultado['segments']:
            inicio = int(segment['start'])
            texto_en = segment['text']
            
            # Traducir frase
            traduccion = translator.translate(texto_en)
            
            # Formato tiempo [MM:SS]
            tiempo = f"{inicio // 60:02d}:{inicio % 60:02d}"
            st.write(f"**[{tiempo}]**: {traduccion}")
            
        cap.release()
        os.remove(output)
        status.success("¡Completado!")
        
    except Exception as e:
        st.error(f"Error: {e}")
