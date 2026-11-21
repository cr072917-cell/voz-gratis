import asyncio
import edge_tts
import streamlit as st

st.set_page_config(page_title="Voz gratis para tus videos", page_icon="🎙️")
st.title("🎙️ Voz gratis para tus videos")
st.caption("Pega tu guion, elige la voz y descarga el audio en MP3.")

VOCES = {
    "Emilio (Rep. Dominicana, hombre)": "es-DO-EmilioNeural",
    "Ramona (Rep. Dominicana, mujer)": "es-DO-RamonaNeural",
    "Jorge (México, hombre)": "es-MX-JorgeNeural",
    "Dalia (México, mujer)": "es-MX-DaliaNeural",
    "Alonso (EE. UU., hombre)": "es-US-AlonsoNeural",
    "Paloma (EE. UU., mujer)": "es-US-PalomaNeural",
    "Álvaro (España, hombre)": "es-ES-AlvaroNeural",
    "Elvira (España, mujer)": "es-ES-ElviraNeural",
}


async def generar(texto: str, voz: str, velocidad: int) -> bytes:
    rate = f"{velocidad:+d}%"
    comm = edge_tts.Communicate(texto, voz, rate=rate)
    audio = b""
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return audio


texto = st.text_area("Guion", height=250, placeholder="Pega aquí tu guion...")

col1, col2 = st.columns(2)
with col1:
    nombre_voz = st.selectbox("Voz", list(VOCES.keys()))
with col2:
    velocidad = st.slider("Velocidad (%)", -30, 30, 0, step=5)

if st.button("Generar voz", type="primary"):
    if not texto.strip():
        st.warning("Escribe o pega un guion primero.")
    else:
        with st.spinner("Generando audio..."):
            try:
                st.session_state["audio"] = asyncio.run(
                    generar(texto.strip(), VOCES[nombre_voz], velocidad)
                )
            except Exception as e:
                st.session_state.pop("audio", None)
                st.error(f"No se pudo generar el audio (¿hay internet?): {e}")

if "audio" in st.session_state:
    st.audio(st.session_state["audio"], format="audio/mp3")
    st.download_button(
        "⬇️ Descargar MP3",
        data=st.session_state["audio"],
        file_name="voz.mp3",
        mime="audio/mpeg",
    )
