import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os

st.set_page_config(page_title="Manual PXN en Español", layout="wide")

def format_time(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    return f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("🎬 Traductor de Instrucciones Visuales")
st.write("Pegá el link de Drive. Esta versión está optimizada para el tutorial del volante PXN.")

drive_url = st.text_input("Link de Google Drive:")

if drive_url and st.button("Generar Manual"):
    with st.spinner("Leyendo video... por favor espera."):
        try:
            output = 'video_tutorial.mp4'
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            # Cargamos el lector (inglés) y el traductor
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            
            cap = cv2.VideoCapture(output)
            fps = cap.get(cv2.CAP_PROP_FPS)
            textos_vistos = set()
            count = 0

            st.subheader("Manual de Instrucciones Traducido:")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # Analizamos cada 1 segundo
                if count % int(fps) == 0:
                    h, w, _ = frame.shape
                    
                    # CORTAR: Nos enfocamos solo en la franja negra de abajo donde están las letras
                    # Esto evita que las luces LED del fondo confundan a la IA
                    corte = frame[int(h*0.82):int(h*0.95), :] 
                    
                    # Mejoramos el contraste del corte para que las letras se vean mejor
                    gray = cv2.cvtColor(corte, cv2.COLOR_BGR2GRAY)
                    
                    res = reader.readtext(gray, detail=0, paragraph=True)
                    texto_en = " ".join(res).strip()
                    
                    # Filtro: Solo si tiene más de 10 letras (instrucciones reales)
                    if len(texto_en) > 10 and texto_en not in textos_vistos:
                        try:
                            traduccion = translator.translate(texto_en)
                            # Limpieza simple de símbolos raros
                            traduccion_limpia = "".join(c for c in traduccion if c.isalnum() or c in " ,.?!:áéíóúñÁÉÍÓÚÑ")
                            
                            st.write(f"**{format_time(count//fps)}**: {traduccion_limpia}")
                            textos_vistos.add(texto_en)
                        except: continue
                count += 1
            
            cap.release()
            os.remove(output)
            st.success("¡Análisis finalizado!")

        except Exception as e:
            st.error(f"Se produjo un aviso: {str(e)}")
