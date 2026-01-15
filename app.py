import streamlit as st
import whisper
import os
from deep_translator import GoogleTranslator
import re

def format_time_srt(srt_time):
    # Limpia el tiempo de 00:00:01,000 a "segundo 1"
    try:
        parts = srt_time.split(':')
        mins = int(parts[1])
        secs = int(float(parts[2].replace(',', '.')))
        total_seconds = mins * 60 + secs
        if total_seconds < 60: return f"segundo {total_seconds}"
        return f"minuto {total_seconds // 60}:{total_seconds % 60:02d}"
    except:
        return "Tiempo desconocido"

st.set_page_config(page_title="Traductor Profesional", page_icon="🎬")
st.title("🎬 Traductor de Subtítulos (.srt)")

srt_file = st.file_uploader("Sube tu archivo .srt en inglés:", type=["srt"])

if srt_file and st.button("Traducir ahora"):
    st.write("### 📝 Traducción al Español Neutro:")
    
    # Leer el archivo y separar por bloques de subtítulos
    raw_content = srt_file.getvalue().decode("utf-8")
    # Dividir el archivo donde haya números seguidos de tiempos (formato SRT)
    bloques = re.split(r'\n\s*\n', raw_content.strip())
    
    translator = GoogleTranslator(source='en', target='es')
    
    for bloque in bloques:
        lineas = bloque.splitlines()
        # Un bloque SRT válido tiene al menos: 1.Número, 2.Tiempo, 3.Texto
        if len(lineas) >= 3:
            # 1. Buscar la línea del tiempo (contiene -->)
            linea_tiempo = ""
            texto_ingles = ""
            for l in lineas:
                if "-->" in l:
                    linea_tiempo = l
                elif not l.strip().isdigit() and "-->" not in l:
                    texto_ingles += l + " "
            
            if linea_tiempo and texto_ingles.strip():
                # Limpiar texto de etiquetas como [Music] o ruidos
                texto_limpio = re.sub(r'\[.*?\]', '', texto_ingles).strip()
                
                if texto_limpio:
                    # Traducir
                    tiempo_inicio = linea_tiempo.split(" --> ")[0]
                    tiempo_formateado = format_time_srt(tiempo_inicio)
                    
                    try:
                        traduccion = translator.translate(texto_limpio)
                        st.write(f"**{tiempo_formateado}**: {traduccion}")
                    except:
                        continue

st.info("Nota: Si el video es muy largo, la traducción puede tardar unos segundos en aparecer completa.")
