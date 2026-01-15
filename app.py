import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import re

st.set_page_config(page_title="Traductor de Subtítulos YouTube", layout="centered")

st.title("🎬 Traductor de Subtítulos YouTube")
st.write("Pegá un link de YouTube con subtítulos en inglés y obtené la traducción minuto a minuto.")

translator = Translator()

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

youtube_url = st.text_input("🔗 Link del video de YouTube")

if st.button("Traducir subtítulos"):
    if not youtube_url:
        st.error("Pegá un link de YouTube válido.")
    else:
        video_id = extract_video_id(youtube_url)

        if not video_id:
            st.error("No se pudo detectar el ID del video.")
        else:
            try:
                with st.spinner("Obteniendo subtítulos..."):
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

                st.success("Subtítulos encontrados. Traduciendo...")

                output = []

                for entry in transcript:
                    start = int(entry["start"])
                    text_en = entry["text"].replace("\n", " ")

                    text_es = translator.translate(text_en, src="en", dest="es").text

                    if start < 60:
                        time_label = f"segundo {start}"
                    else:
                        time_label = f"minuto {start // 60}:{start % 60:02d}"

                    output.append(f"{time_label}: {text_es}")

                st.text_area(
                    "Resultado final",
                    value="\n".join(output),
                    height=400
                )

            except Exception as e:
                st.error("No se pudieron obtener los subtítulos. Verificá que el video tenga subtítulos en inglés.")
