import streamlit as st
from deep_translator import GoogleTranslator
import re

def limpiar_tiempo(texto_tiempo):
    try:
        match = re.search(r'(\d{2}):(\d{2}):(\d{2})', texto_tiempo)
        if match:
            horas, minutos, segundos = map(int, match.groups())
            total = (horas * 3600) + (minutos * 60) + segundos
            if total < 60: return f"segundo {total}"
            return f"minuto {total // 60}:{total % 60:02d}"
    except: return "Tiempo"
    return "Tiempo"

st.set_page_config(page_title="Traductor Profesional", page_icon="🎬")
st.title("🎬 Traductor de Subtítulos (.srt)")

archivo = st.file_uploader("Sube tu archivo .srt aquí:", type=["srt"])

if archivo and st.button("Traducir Todo el Video"):
    st.write("### 📝 Traducción al Español Neutro:")
    
    lineas = archivo.getvalue().decode("utf-8", errors="ignore").splitlines()
    translator = GoogleTranslator(source='en', target='es')
    
    tiempo_actual = ""
    encontró_texto = False

    for linea in lineas:
        linea = linea.strip()
        
        if "-->" in linea:
            tiempo_actual = limpiar_tiempo(linea.split("-->")[0])
        
        elif linea and not linea.isdigit() and "-->" not in linea:
            # 1. Eliminar ruidos entre corchetes o paréntesis
            linea_limpia = re.sub(r'\[.*?\]|\(.*?\)', '', linea).strip()
            
            # 2. FILTRO CLAVE: Solo traducir si la frase tiene sentido (más de 2 letras)
            # Esto elimina los "a", "w", "oh", "v" que te molestan
            if len(linea_limpia) > 2:
                try:
                    traduccion = translator.translate(linea_limpia)
                    if traduccion.lower() not in ['a', 'w', 'oh', 'v', 'y']:
                        st.write(f"**{tiempo_actual}**: {traduccion}")
                        encontró_texto = True
                except:
                    continue

    if not encontró_texto:
        st.warning("⚠️ El archivo SRT parece no tener diálogos reales, solo sonidos ambientales.")

st.info("Tip: Si el video tiene poca voz, asegúrate de descargar el SRT de 'English' y no el 'English (auto-generated)' si está disponible.")
