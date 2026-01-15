import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import gdown
import os
import re

st.set_page_config(page_title="Traductor Visual PXN", layout="wide")

def es_texto_valido(texto):
    # Filtro para ignorar códigos raros y símbolos
    if len(texto) < 5: return False
    caracteres_raros = re.findall(r'[^\w\s,.!?:áéíóúÁÉÍÓÚñÑ]', texto)
    if len(caracteres_raros) > len(texto) * 0.3: return False
    return True

def format_time(seconds):
    seconds = int(seconds)
    return f"segundo {seconds}" if seconds < 60 else f"minuto {seconds // 60}:{seconds % 60:02d}"

st.title("🎬 Traductor de Tutoriales (Versión Limpia)")
st.write("Pegá el link de Drive y el programa filtrará solo las instrucciones reales.")

drive_url = st.text_input("Link de Google Drive:")

if drive_url and st.button("Empezar Traducción"):
    with st.spinner("Analizando y limpiando texto..."):
        try:
            output = 'video_final.mp4'
            gdown.download(url=drive_url, output=output, quiet=False, fuzzy=True)
            
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            cap = cv2.VideoCapture(output)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            historial_traduccion = []
            textos_vistos = set()
            count = 0

            st.subheader("Manual de Instrucciones:")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                if count % int(fps) == 0:
                    h, w, _ = frame.shape
                    corte = frame[int(h*0.65):int(h*0.92), :]
                    
                    res = reader.readtext(corte, detail=0)
                    texto_en = " ".join(res).strip()
                    
                    # Aplicamos el filtro de limpieza
                    if es_texto_valido(texto_en) and texto_en not in textos_vistos:
                        try:
                            traduccion = translator.translate(texto_en)
                            tiempo = format_time(count // fps)
                            linea = f"**{tiempo}**: {traduccion}"
                            st.write(linea)
                            historial_traduccion.append(f"{tiempo}: {traduccion}")
                            textos_vistos.add(texto_en)
                        except: continue
                count += 1
            
            cap.release()
            os.remove(output)
            
            if historial_traduccion:
                st.success("¡Análisis terminado!")
                # Botón para descargar el manual
                manual_texto = "\n".join(historial_traduccion)
                st.download_button("📥 Descargar Manual Traducido (.txt)", manual_texto, file_name="manual_pxn_espanol.txt")

        except Exception as e:
            st.error(f"Hubo un aviso: {str(e)}")
