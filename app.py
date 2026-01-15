import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

# Configuración de página
st.set_page_config(page_title="Traductor Visual Pro", layout="centered")

def format_time(seconds):
    return f"segundo {seconds}" if seconds < 60 else f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("🎬 Lector de Subtítulos Pegados")
st.write("Copiá el link de tu video en Google Drive (aseguráte que sea público).")

# Campo para el link
drive_url = st.text_input("Link de Google Drive:")

if drive_url and st.button("Traducir Video"):
    with st.spinner("Descargando y analizando... esto puede tardar unos minutos."):
        try:
            output = 'video_simracing.mp4'
            # gdown descarga el video de Drive directamente al servidor
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            # IA Visual
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
                
                # Analiza 1 vez por segundo
                if count % int(fps) == 0:
                    h, w, _ = frame.shape
                    # Recorte de la zona de abajo (subtítulos)
                    corte = frame[int(h*0.75):h, :]
                    
                    res = reader.readtext(corte, detail=0)
                    texto_en = " ".join(res).strip()
                    
                    if len(texto_en) > 3 and texto_en not in textos_vistos:
                        traduccion = translator.translate(texto_en)
                        st.write(f"**{format_time(count//fps)}**: {traduccion}")
                        textos_vistos.add(texto_en)
                count += 1
            
            cap.release()
            if os.path.exists(output):
                os.remove(output)
            st.success("¡Listo!")

        except Exception as e:
            st.error(f"Error: {e}")
