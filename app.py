import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

# Configuración de la interfaz
st.set_page_config(page_title="Traductor Visual Pro", layout="wide")

def format_time(seconds):
    # Convertimos a entero (int) para evitar el error 'float' que trabó la app
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    return f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("🎬 Traductor de Subtítulos Pegados (vía Drive)")
st.write("La IA está leyendo los textos del video. Asegúrate de que el link de Drive sea público.")

drive_url = st.text_input("Pegá aquí el enlace de compartir de Google Drive:", placeholder="https://drive.google.com/...")

if drive_url and st.button("Empezar Traducción Visual"):
    with st.spinner("Procesando video... Esto puede tardar según la duración."):
        try:
            output = 'video_descargado.mp4'
            # Descarga limpia desde Drive
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            # Motores de IA
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            
            cap = cv2.VideoCapture(output)
            fps = cap.get(cv2.CAP_PROP_FPS)
            textos_vistos = set()
            count = 0

            st.subheader("Traducción paso a paso:")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # Analizamos cada 1 segundo exacto
                if count % int(fps) == 0:
                    h, w, _ = frame.shape
                    # Recorte optimizado para la zona de texto de PXN
                    corte = frame[int(h*0.65):int(h*0.95), :]
                    
                    resultado = reader.readtext(corte, detail=0)
                    texto_en = " ".join(resultado).strip()
                    
                    if len(texto_en) > 3 and texto_en not in textos_vistos:
                        traduccion = translator.translate(texto_en)
                        # Aseguramos que el tiempo enviado a la función sea entero
                        tiempo_seg = int(count // fps)
                        st.write(f"**{format_time(tiempo_seg)}**: {traduccion}")
                        textos_vistos.add(texto_en)
                count += 1
            
            cap.release()
            if os.path.exists(output):
                os.remove(output)
            st.success("¡Análisis completado con éxito!")

        except Exception as e:
            # Mensaje de error más amigable
            st.error(f"Nota: Si el video se detuvo, intenta actualizar la página. Error: {str(e)}")
