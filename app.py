import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import os
import numpy as np

def format_time(seconds):
    return f"segundo {seconds}" if seconds < 60 else f"minuto {seconds // 60}:{seconds % 60:02d}"

st.set_page_config(page_title="Lector de Subtítulos Visuales", page_icon="👁️")
st.title("🎬 Traductor Visual de Tutoriales")
st.write("Esta herramienta lee el texto pegado en la imagen y lo traduce.")

video_file = st.file_uploader("Sube el video del volante PXN:", type=["mp4", "mov", "avi"])

if video_file is not None:
    if st.button("Escanear y Traducir"):
        with st.spinner("La IA está leyendo el video cuadro por cuadro..."):
            try:
                # Guardar video temporal
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_file.getbuffer())
                
                # Configurar IA Visual e Idioma
                reader = easyocr.Reader(['en']) # Lee inglés del video
                translator = GoogleTranslator(source='en', target='es')
                
                cap = cv2.VideoCapture("temp_video.mp4")
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                st.subheader("Traducción Paso a Paso:")
                textos_vistos = set()
                count = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    # Escanear 1 vez por segundo para precisión
                    if count % int(fps) == 0:
                        segundo_actual = int(count / fps)
                        
                        # RECORTAR: Nos enfocamos en el área de subtítulos (centro-inferior)
                        h, w, _ = frame.shape
                        zona_texto = frame[int(h*0.65):int(h*0.95), :] 
                        
                        # OCR: Leer el texto
                        resultados = reader.readtext(zona_texto, detail=0)
                        texto_en = " ".join(resultados).strip()
                        
                        # Traducir si hay contenido nuevo
                        if len(texto_en) > 4 and texto_en not in textos_vistos:
                            traduccion = translator.translate(texto_en)
                            st.write(f"**{format_time(segundo_actual)}**: {traduccion}")
                            textos_vistos.add(texto_en)

                    count += 1
                
                cap.release()
                os.remove("temp_video.mp4")
                st.success("¡Análisis completado!")

            except Exception as e:
                st.error(f"Error técnico: {e}")
