import streamlit as st
import whisper
import os

# Configuración de formato de tiempo
def format_time(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"segundo {seconds}"
    else:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"minuto {minutes}:{remaining_seconds:02d}"

st.set_page_config(page_title="Traductor Pro Preciso", page_icon="🏎️")
st.title("🎬 Traductor Pro (Tiempos Corregidos)")
st.write("Esta versión usa el modelo 'Base' para mayor precisión en los segundos.")

uploaded_file = st.file_uploader("Sube tu video o audio:", type=["mp4", "mp3", "m4a", "wav"])

if uploaded_file is not None:
    if st.button("Empezar Traducción"):
        with st.spinner("Analizando con precisión... esto puede tardar un poco más que antes."):
            try:
                # Guardar temporal
                with open("archivo_temp", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # CARGA DE MODELO MÁS PRECISO
                model = whisper.load_model("base")
                
                # Transcripción con parámetros de estabilidad
                # beam_size ayuda a que no se salte el inicio de las frases
                result = model.transcribe("archivo_temp", language="es", beam_size=5)

                st.success("¡Traducción completada!")
                
                # Preparar texto para descargar
                texto_final = ""
                
                for segment in result['segments']:
                    # Solo procesar si hay texto real (evita los segundos 0 fantasmas)
                    frase = segment['text'].strip()
                    if frase:
                        tiempo = format_time(segment['start'])
                        linea = f"**{tiempo}**: {frase}"
                        st.write(linea)
                        texto_final += f"{tiempo}: {frase}\n"

                # Botón para descargar el resultado
                st.download_button(
                    label="Descargar traducción (.txt)",
                    data=texto_final,
                    file_name="traduccion.txt",
                    mime="text/plain"
                )

                if os.path.exists("archivo_temp"):
                    os.remove("archivo_temp")

            except Exception as e:
                st.error(f"Error: {e}")
