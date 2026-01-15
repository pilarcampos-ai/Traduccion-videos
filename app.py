import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

st.set_page_config(page_title="Manual PXN", layout="centered")

st.title("🎬 Traductor Visual PXN")
st.write("Copia el link de Drive y genera tu manual paso a paso.")

url_drive = st.text_input("Link de Google Drive:")

if url_drive and st.button("Empezar Manual"):
    try:
        archivo_temp = "video.mp4"
        # Descarga el video
        gdown.download(url=url_drive, output=archivo_temp, quiet=False, fuzzy=True)
        
        # Cargamos IA
        reader = easyocr.Reader(['en'])
        translator = GoogleTranslator(source='en', target='es')
        
        video = cv2.VideoCapture(archivo_temp)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        
        textos_listos = []
        contador = 0
        
        st.subheader("Instrucciones detectadas:")

        while video.isOpened():
            ret, frame = video.read()
            if not ret: break
            
            # Analiza cada 1 segundo exacto
            if contador % fps == 0:
                h, w, _ = frame.shape
                # CORTE DINÁMICO: Solo la franja de abajo donde están los textos
                recorte = frame[int(h*0.80):int(h*0.95), :]
                
                # Leer texto (sin filtros raros que rompan todo)
                resultado = reader.readtext(recorte, detail=0)
                texto_en = " ".join(resultado).strip()
                
                # Si hay texto y es largo, lo traducimos
                if len(texto_en) > 8 and texto_en not in textos_listos:
                    traduccion = translator.translate(texto_en)
                    segundo = contador // fps
                    # Formato de tiempo simple para que no de error de 'float'
                    tiempo = f"{segundo // 60:02d}:{segundo % 60:02d}"
                    st.write(f"**[{tiempo}]**: {traduccion}")
                    textos_listos.append(texto_en)
            
            contador += 1
            
        video.release()
        os.remove(archivo_temp)
        st.success("¡Manual finalizado!")
        
    except Exception as e:
        st.error(f"Hubo un problema. Intenta recargar la página. Error: {e}")
