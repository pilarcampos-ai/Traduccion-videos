import streamlit as st
import whisper
import os

def format_time(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    else:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"minuto {minutes}:{remaining_seconds:02d}"

st.set_page_config(page_title="Traductor Pro", page_icon="🎬")
st.title("🎬 Traductor por Archivo (Versión Estable)")

uploaded_file = st.file_uploader("Sube tu video o audio aquí:", type=["mp4", "mp3", "m4a", "wav"])

if uploaded_file is not None:
    if st.button("Empezar Traducción"):
        with st.spinner("Traduciendo..."):
            try:
                # 1. Guardar archivo
                with open("archivo_temp", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 2. Usamos 'tiny' de nuevo (EL QUE FUNCIONA)
                model = whisper.load_model("tiny")
                
                # 3. TRUCO PARA EL TIEMPO: 
                # Agregamos initial_prompt para que la IA entienda mejor el inicio
                result = model.transcribe("archivo_temp", language="es", initial_prompt="Traducción técnica de simracing.")

                st.subheader("Resultado:")
                
                for segment in result['segments']:
                    # Arreglo: Solo muestra si el tiempo es mayor a 0.5 o tiene texto real
                    # Esto evita que el primer subtítulo diga "0" si el audio empieza después
                    if segment['start'] < 0.5 and not segment['text'].strip():
                        continue
                    
                    st.write(f"**{format_time(segment['start'])}**: {segment['text'].strip()}")

                if os.path.exists("archivo_temp"):
                    os.remove("archivo_temp")

            except Exception as e:
                st.error(f"Error: {e}")
