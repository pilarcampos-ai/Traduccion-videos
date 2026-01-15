import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

# Configuración para que la app sea ancha y se vea bien
st.set_page_config(page_title="Traductor Visual Pro", layout="wide")

def format_time(seconds):
    return f"segundo {seconds}" if seconds < 60 else f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("🎬 Traductor de Subtítulos Pegados (vía Drive)")
st.write("Usa esta opción para videos pesados. El programa leerá el texto de la imagen.")

# Entrada para el link de Google Drive
drive_url = st.text_input("Pegá aquí el enlace de compartir de Google Drive:")

if drive_url and st.button("Empezar Traducción Visual"):
    with st.spinner("Descargando video y activando IA Visual..."):
        try:
            output = 'video_descargado.mp4'
            # gdown descarga el archivo directamente de Drive al servidor
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            # Cargamos el motor de lectura visual
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            
            cap = cv2.VideoCapture(output)
            fps = cap.get(cv2.CAP_PROP_FPS)
            textos_vistos = set()
            count = 0

            st.subheader("Traducción segundo a segundo:")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # Analizamos 1 cuadro por segundo
                if count % int(fps) == 0:
                    h, w, _ = frame.shape
                    # RECORTAMOS la zona de abajo (donde están los subtítulos en tu video)
                    corte = frame[int(h*0.75):h, :]
                    
                    # Extraer texto de la imagen
                    resultado = reader.readtext(corte, detail=0)
                    texto_en = " ".join(resultado).strip()
                    
                    if len(texto_en) > 3 and texto_en not in textos_vistos:
                        traduccion = translator.translate(texto_en)
                        st.write(f"**{format_time(count//fps)}**: {traduccion}")
                        textos_vistos.add(texto_en)
                count += 1
            
            cap.release()
            if os.path.exists(output):
                os.remove(output)
            st.success("¡Análisis completado!")

        except Exception as e:
            st.error(f"Error: Asegúrate de que el link de Drive sea PÚBLICO. Detalle: {e}")
