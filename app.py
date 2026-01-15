import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import numpy as np

st.title("🎬 Traductor de Subtítulos Pegados (OCR)")
st.write("Usa esto para videos que NO tienen voz, solo texto en pantalla.")

file = st.file_uploader("Sube el video:", type=["mp4", "mov", "avi"])

if file is not None:
    if st.button("Escanear y Traducir Texto Visual"):
        with st.spinner("Escaneando fotogramas... esto puede tardar."):
            # Guardar video temporal
            with open("temp_video.mp4", "wb") as f:
                f.write(file.getbuffer())
            
            cap = cv2.VideoCapture("temp_video.mp4")
            reader = easyocr.Reader(['en', 'es']) # Lee inglés y español
            translator = GoogleTranslator(source='en', target='es')
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            count = 0
            textos_detectados = set()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # Escaneamos 1 frame por cada segundo para no colapsar la memoria
                if count % int(fps) == 0:
                    results = reader.readtext(frame)
                    for (bbox, text, prob) in results:
                        if len(text) > 3 and text not in textos_detectados:
                            segundo = int(count / fps)
                            traduccion = translator.translate(text)
                            st.write(f"**Segundo {segundo}**: {traduccion}")
                            textos_detectados.add(text)
                count += 1
            
            cap.release()
