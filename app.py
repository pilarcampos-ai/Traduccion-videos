import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import numpy as np
import os

# Función para convertir segundos a tu formato preferido
def format_time(seconds):
    if seconds < 60:
        return f"segundo {seconds}"
    return f"minuto {seconds // 60}:{seconds % 60:02d}"

st.set_page_config(page_title="Traductor Visual Pro", page_icon="👁️")
st.title("👁️ Traductor de Texto en Pantalla")
st.write("Ideal para videos sin voz pero con subtítulos pegados en la imagen.")

video_file = st.file_uploader("Sube tu video aquí:", type=["mp4", "mov", "avi"])

if video_file is not None:
    if st.button("Escanear y Traducir"):
        with st.spinner("Leyendo los subtítulos del video..."):
            try:
                # 1. Guardar el video para que el sistema pueda leerlo
                with open("video_proceso.mp4", "wb") as f:
                    f.write(video_file.getbuffer())
                
                # 2. Configurar el lector visual (Inglés)
                reader = easyocr.Reader(['en'])
                translator = GoogleTranslator(source='en', target='es')
                
                cap = cv2.VideoCapture("video_proceso.mp4")
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                st.subheader("Traducción minuto a minuto:")
                textos_vistos = set()
                count = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    # Analizamos el video 1 vez por segundo para que sea rápido
                    if count % int(fps) == 0:
                        segundo_actual = int(count / fps)
                        
                        # RECORTAR LA IMAGEN: Enfocamos solo la parte de abajo (donde están los subs)
                        alto, ancho, _ = frame.shape
                        zona_subtitulos = frame[int(alto*0.70):alto, :] 
                        
                        # Leer texto de la imagen
                        resultado = reader.readtext(zona_subtitulos, detail=0)
                        texto_en = " ".join(resultado).strip()
                        
                        # Si detectamos texto nuevo y largo, traducimos
                        if len(texto_en) > 3 and texto_en not in textos_vistos:
                            traduccion = translator.translate(texto_en)
                            st.write(f"**{format_time(segundo_actual)}**: {traduccion}")
                            textos_vistos.add(texto_en)

                    count += 1
                
                cap.release()
                os.remove("video_proceso.mp4")
                st.success("¡Lectura completada!")

            except Exception as e:
                st.error(f"Error al procesar: {e}")
