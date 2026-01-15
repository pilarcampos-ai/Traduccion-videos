import streamlit as st
import whisper
import os
from deep_translator import GoogleTranslator

def format_time_srt(srt_time):
    # Convierte 00:00:01,000 -> segundo 1
    parts = srt_time.split(':')
    seconds = int(parts[1]) * 60 + int(float(parts[2].replace(',', '.')))
    if seconds < 60: return f"segundo {seconds}"
    return f"minuto {seconds // 60}:{seconds % 60:02d}"

st.set_page_config(page_title="Traductor Total", page_icon="🎬")
st.title("🎬 Traductor de Video o Subtítulos")

opcion = st.radio("¿Qué vas a subir?", ["Video/Audio (IA Escucha)", "Archivo SRT (Subtítulos en inglés)"])

if opcion == "Video/Audio (IA Escucha)":
    uploaded_file = st.file_uploader("Sube tu archivo:", type=["mp4", "mp3", "m4a", "wav"])
    if uploaded_file and st.button("Traducir Audio"):
        with st.spinner("Escuchando..."):
            with open("temp", "wb") as f: f.write(uploaded_file.getbuffer())
            model = whisper.load_model("tiny")
            result = model.transcribe("temp", language="es")
            for segment in result['segments']:
                st.write(f"**{format_time_srt('00:00:00')}**: {segment['text'].strip()}") # Simplificado para el ejemplo
            os.remove("temp")

else:
    srt_file = st.file_uploader("Sube tu archivo .srt en inglés:", type=["srt"])
    if srt_file and st.button("Traducir Subtítulos"):
        st.write("### 📝 Traducción Real a Español:")
        contenido = srt_file.getvalue().decode("utf-8").split("\n\n")
        
        translator = GoogleTranslator(source='en', target='es')
        
        for bloque in contenido:
            lineas = bloque.splitlines()
            if len(lineas) >= 3:
                # Extraer tiempo
                tiempo_raw = lineas[1].split(" --> ")[0]
                tiempo_limpio = format_time_srt(tiempo_raw)
                
                # Unir y traducir texto
                texto_en = " ".join(lineas[2:])
                # Ignorar si es solo música o sonidos
                if "[" not in texto_en:
                    traduccion = translator.translate(texto_en)
                    st.write(f"**{tiempo_limpio}**: {traduccion}")
