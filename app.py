import streamlit as st
import random


def cargar_preguntas(nombre_archivo):
    preguntas = []

    with open(nombre_archivo, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    i = 0
    while i < len(lineas) - 1:
        pregunta = lineas[i]
        respuesta = lineas[i + 1]

        if respuesta.startswith("(Respuesta):"):
            respuesta = respuesta.replace("(Respuesta):", "").strip()
            preguntas.append((pregunta, respuesta))

        i += 2

    return preguntas


archivos_categorias = {
    "Medicina": "preguntas_medicina.txt",
    "Historia": "preguntas_historia.txt",
    "Literatura": "preguntas_literatura.txt",
    "Geografia": "preguntas_geografia.txt",
}

st.title("Preguntas aleatorias")

categoria = st.selectbox(
    "Elegí una categoría",
    ["Todas"] + list(archivos_categorias.keys())
)

preguntas = []

if categoria == "Todas":
    for archivo in archivos_categorias.values():
        preguntas.extend(cargar_preguntas(archivo))
else:
    preguntas = cargar_preguntas(archivos_categorias[categoria])

if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = None

if st.button("Nueva pregunta"):
    st.session_state.pregunta_actual = random.choice(preguntas)

if st.session_state.pregunta_actual:
    st.subheader(st.session_state.pregunta_actual[0])

    if st.button("Mostrar respuesta"):
        st.success(st.session_state.pregunta_actual[1])