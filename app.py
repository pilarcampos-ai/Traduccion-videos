import streamlit as st
from deep_translator import GoogleTranslator
import re

def limpiar_y_formatear(tiempo_raw):
    # Pasa de 00:00:01,000 a "segundo 1"
    try:
        segmentos = tiempo_raw.split(':')
        segundos = int(segmentos[1]) * 60 + int(float(segmentos[2].replace(',', '.')))
        return f"segundo {segundos}" if segundos < 60 else f"minuto {segundos // 60}:{segundos % 60:02d}"
    except:
        return "Tiempo"

st.set_page_config(page_title="Traductor Real", page_icon="🎬")
st.title("🎬 Traductor de Subtítulos Pro")

archivo = st.file_uploader("Sube tu archivo .srt aquí:", type=["srt"])

if archivo and st.button("Traducir Todo"):
    st.write("### 📝 Traducción al Español Neutro:")
    
    # Leemos el archivo ignorando errores de símbolos raros
    lineas = archivo.getvalue().decode("utf-8", errors="ignore").splitlines()
    translator = GoogleTranslator(source='en', target='es')
    
    tiempo_actual = ""
    texto_para_traducir = []

    for linea in lineas:
        linea = linea.strip()
        
        # Detectar la línea de tiempo
        if "-->" in linea:
            # Si ya teníamos texto acumulado de antes, lo traducimos antes de pasar al siguiente tiempo
            tiempo_actual = limpiar_y_formatear(linea.split("-->")[0].strip())
        
        # Detectar el texto (si no es tiempo, ni número, ni está vacío)
        elif linea and not linea.isdigit() and "-->" not in linea:
            # Eliminar etiquetas como [Music], [Applause], etc.
            limpio = re.sub(r'\[.*?\]', '', linea).strip()
            
            if limpio and len(limpio) > 1: # Ignora letras sueltas como "a" o "w"
                try:
                    traduccion = translator.translate(limpio)
                    st.write(f"**{tiempo_actual}**: {traduccion}")
                except:
                    continue

st.info("Esta versión filtra ruidos y traduce frases completas.")
