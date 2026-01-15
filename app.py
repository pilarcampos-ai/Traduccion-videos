import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import numpy as np
import os

st.set_page_config(page_title="Traductor Visual", page_icon="👁️")
st.title("👁️ Traductor de Subtítulos Pegados")
st.write("Para videos sin voz con texto integrado en la imagen.")

# Aumentar límite de subida a 200MB (Límite de Streamlit Cloud)
file = st.file_uploader("Sube el video (Máx 200MB):", type=["mp4", "mov", "avi"])

if file is not None:
    if st.button("Escanear Texto del Video"):
        with st.spinner("Leyendo fotogramas... Esto es un proceso visual y toma tiempo."):
            try:
                # Guardar temporal
                with open("temp_v.mp4", "wb") as f:
                    f.write(file.getbuffer())
                
                cap = cv2.VideoCapture("temp_v.mp4")
                # Inicializar lector de imágenes (OCR)
                reader = easyocr.Reader(['en']) 
                translator = GoogleTranslator(source='en', target='es')
                
                fps = cap.get(cv2.CAP_PROP_FPS)
                count = 0
                ultimos_textos = []

                st.subheader("Traducción Visual Detectada:")

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    # Analizar 1 frame por cada segundo para no colapsar la app
                    if count % int(fps) == 0:
                        segundo = int(count / fps)
                        # Detectar texto en el frame
                        result = reader.readtext(frame, detail=0)
                        
                        if result:
                            texto_unido = " ".join(result).strip()
                            # Solo traducir si el texto es nuevo y tiene longitud real
                            if len(texto_unido) > 3 and texto_unido not in ultimos_textos:
                                traduccion = translator.translate(texto_unido)
                                st.write(f"**Segundo {segundo}**: {traduccion}")
                                # Guardamos los últimos para no repetir lo mismo
                                ultimos_textos.append(texto_unido)
                                if len(ultimos_textos) > 5: ultimos_textos.pop(0)

                    count += 1
                
                cap.release()
                os.remove("temp_v.mp4")
            except Exception as e:
                st.error(f"Error: {e}")
