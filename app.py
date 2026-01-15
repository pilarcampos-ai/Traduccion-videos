import streamlit as st
import cv2
import easyocr
from deep_translator import GoogleTranslator
import yt_dlp
import os

st.title("👁️ Traductor Visual de YouTube")

# Usamos el link para que TÚ no tengas que subir el archivo pesado
url = st.text_input("Pega el link de YouTube aquí:")

if url and st.button("Analizar Video"):
    with st.spinner("Descargando video internamente para analizarlo..."):
        try:
            # Configuramos para bajar el video en la calidad más baja (para ir rápido)
            ydl_opts = {
                'format': 'worst', 
                'outtmpl': 'video_a_leer.mp4',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Ahora iniciamos el OCR (Lectura de imagen)
            reader = easyocr.Reader(['en'])
            translator = GoogleTranslator(source='en', target='es')
            cap = cv2.VideoCapture('video_a_leer.mp4')
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            st.subheader("Traducción del texto pegado:")
            textos_vistos = set()
            count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                if count % int(fps) == 0: # Analiza 1 segundo por vez
                    # Recorte de la zona inferior (subtítulos)
                    h, w, _ = frame.shape
                    corte = frame[int(h*0.75):h, :]
                    
                    resultado = reader.readtext(corte, detail=0)
                    texto_en = " ".join(resultado).strip()
                    
                    if len(texto_en) > 3 and texto_en not in textos_vistos:
                        traduccion = translator.translate(texto_en)
                        st.write(f"**Min {int(count/fps/60)}:{int(count/fps%60):02d}**: {traduccion}")
                        textos_vistos.add(texto_en)
                count += 1
            
            cap.release()
            os.remove('video_a_leer.mp4')

        except Exception as e:
            st.error(f"Error: {e}")
