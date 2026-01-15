import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

def format_time(seconds):
    return f"segundo {seconds}" if seconds < 60 else f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("👁️ Traductor Visual vía Google Drive")
st.write("Pega el link de compartir de tu video de Drive aquí abajo.")

# Entrada del link de Drive
drive_url = st.text_input("Link de Google Drive:")

if drive_url and st.button("Analizar desde Drive"):
    with st.spinner("Descargando video desde Drive..."):
        try:
            # Convertimos el link de compartir en un link de descarga directa
            output = 'video_drive.mp4'
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            # Iniciamos el proceso visual que ya conoces
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            cap = cv2.VideoCapture(output)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            st.subheader("Traducción segundo a segundo:")
            textos_vistos = set()
            count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                if count % int(fps) == 0:
                    # Recorte de la franja de subtítulos pegados
                    h, w, _ = frame.shape
                    corte = frame[int(h*0.75):h, :]
                    
                    res = reader.readtext(corte, detail=0)
                    texto_en = " ".join(res).strip()
                    
                    if len(texto_en) > 3 and texto_en not in textos_vistos:
                        traduccion = translator.translate(texto_en)
                        st.write(f"**{format_time(count//fps)}**: {traduccion}")
                        textos_vistos.add(texto_en)
                count += 1
            
            cap.release()
            os.remove(output)
            st.success("¡Análisis terminado!")

        except Exception as e:
            st.error(f"Error: Asegúrate de que el link sea público. Detalle: {e}")
