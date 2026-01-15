import streamlit as st
from deep_translator import GoogleTranslator
import re

def limpiar_tiempo(texto_tiempo):
    # Transforma "00:00:03,500" en "segundo 3"
    try:
        match = re.search(r'(\d{2}):(\d{2}):(\d{2})', texto_tiempo)
        if match:
            horas, minutos, segundos = map(int, match.groups())
            total = (horas * 3600) + (minutos * 60) + segundos
            if total < 60: return f"segundo {total}"
            return f"minuto {total // 60}:{total % 60:02d}"
    except:
        return "Tiempo"
    return "Tiempo"

st.set_page_config(page_title="Traductor SRT Pro", page_icon="🎬")
st.title("🎬 Traductor de Subtítulos (.srt)")

archivo = st.file_uploader("Sube tu archivo .srt aquí:", type=["srt"])

if archivo and st.button("Traducir Todo el Video"):
    st.write("### 📝 Traducción al Español Neutro:")
    
    # Leer el archivo completo
    lineas = archivo.getvalue().decode("utf-8", errors="ignore").splitlines()
    
    translator = GoogleTranslator(source='en', target='es')
    
    texto_acumulado = ""
    tiempo_actual = ""

    for linea in lineas:
        linea = linea.strip()
        
        # 1. Si la línea tiene la flecha de tiempo "-->"
        if "-->" in linea:
            tiempo_actual = limpiar_tiempo(linea.split("-->")[0])
        
        # 2. Si es una línea de texto (no es número solo, no está vacía, no es tiempo)
        elif linea and not linea.isdigit() and "-->" not in linea:
            # Limpiar ruidos como [Music] o [Applause]
            linea_limpia = re.sub(r'\[.*?\]', '', linea).strip()
            if linea_limpia:
                try:
                    # Traducir frase por frase
                    traduccion = translator.translate(linea_limpia)
                    st.write(f"**{tiempo_actual}**: {traduccion}")
                except:
                    st.write(f"**{tiempo_actual}**: {linea_limpia} (Error al traducir)")

st.info("Si el video es largo, dale un momento para procesar todas las líneas.")
