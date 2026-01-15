import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

st.set_page_config(page_title="Traductor Rápido")
st.title("🎬 Traductor Visual (Modo Ligero)")

url_drive = st.text_input("Enlace de Google Drive:")

if url_drive and st.button("Empezar"):
    # Usamos un contenedor para que veas que la app está viva
    status = st.empty()
    status.info("Descargando video...")
    
    try:
        output = "v.mp4"
        gdown.download(url=url_drive, output=output, quiet=False, fuzzy=True)
        
        # Iniciamos el lector (solo una vez para no gastar RAM)
        reader = easyocr.Reader(['en'], gpu=False) # Forzamos a que no use GPU (más lento pero no se cae)
        translator = GoogleTranslator(source='en', target='es')
        
        cap = cv2.VideoCapture(output)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        count = 0
        vistos = set()

        status.success("Analizando... (puedes ver los resultados abajo)")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Analiza cada 2 SEGUNDOS para ir más rápido y no saturar el servidor
            if count % (fps * 2) == 0:
                h, w, _ = frame.shape
                # Miramos solo la parte de abajo
                corte = frame[int(h*0.80):int(h*0.95), :]
                
                res = reader.readtext(corte, detail=0)
                txt = " ".join(res).strip()
                
                if len(txt) > 8 and txt not in vistos:
                    traduccion = translator.translate(txt)
                    st.write(f"**{count//fps//60}:{count//fps%60:02d}** -> {traduccion}")
                    vistos.add(txt)
            count += 1
            
        cap.release()
        os.remove(output)
        status.info("¡Análisis terminado!")

    except Exception as e:
        st.error(f"Error: {e}")
