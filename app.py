import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

st.set_page_config(page_title="Traductor Visual PXN", layout="centered")

def format_time(seconds):
    return f"segundo {seconds}" if seconds < 60 else f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("🎬 Lector Visual de Tutoriales")
st.write("Pegá el link de tu video de Google Drive (aseguráte que sea público).")

# Campo para el link de Drive
drive_url = st.text_input("Link de Google Drive:")

if drive_url and st.button("Traducir Video"):
    with st.spinner("Descargando y analizando visualmente..."):
        try:
            output = 'video_tutorial.mp4'
            # gdown descarga el video de Drive directamente
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            # IA Visual (OCR)
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            
            cap = cv2.VideoCapture(output)
            fps = cap.get(cv2.CAP_PROP_FPS)
            textos_vistos = set()
            count = 0

            st.subheader("Traducción Paso a Paso:")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # Analiza cada 1 segundo para encontrar texto pegado en la imagen
                if count % int(fps) == 0:
                    h, w, _ = frame.shape
                    # RECORTA la zona donde aparecen los subtítulos en el video del PXN
                    corte = frame[int(h*0.65):int(h*0.95), :]
                    
                    res = reader.readtext(corte, detail=0)
                    texto_en = " ".join(res).strip()
                    
                    if len(texto_en) > 4 and texto_en not in textos_vistos:
                        traduccion = translator.translate(texto_en)
                        st.write(f"**{format_time(count//fps)}**: {traduccion}")
                        textos_vistos.add(texto_en)
                count += 1
            
            cap.release()
            if os.path.exists(output):
                os.remove(output)
            st.success("¡Tutorial traducido!")

        except Exception as e:
            st.error(f"Error: Asegurate que el link sea público. Detalle: {e}")
