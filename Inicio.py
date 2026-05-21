import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Análisis de Suelos Agrícolas · Colombia",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS coherente con el resto del proyecto ──────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f4f6f1 !important; color: #1b4332 !important; }
    .stApp p, .stApp span, .stApp label, .stApp li, .stApp small,
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stCaptionContainer"] *,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
    .stCaption, .stCaption *, h1, h2, h3, h4, h5, h6 {
        color: #222222 !important;
    }
    [data-testid="stMarkdownContainer"] strong { color: #1b4332 !important; }
    [data-testid="stDataFrame"] * { color: #222222 !important; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown * { color: #d8f3dc !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌱 Proyecto Integrador: Análisis de Suelos Agrícolas en Colombia")
st.subheader("Caracterización fisicoquímica de suelos · 2014–2024")

st.divider()

# ── 1. Introducción ───────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    st.header("📖 Introducción")
    st.write("""
    Este proyecto analiza un conjunto de **92,738 registros** de análisis de suelos agrícolas
    recolectados en Colombia entre los años **2014 y 2024**. Los datos abarcan cultivos como
    cacao, café, aguacate y caña panelera, distribuidos en **33 departamentos** del país.

    A través de técnicas de **Analítica de Datos** y **Análisis Exploratorio (EDA)**, este tablero
    permite comprender la calidad fisicoquímica del suelo, identificar deficiencias de nutrientes
    y apoyar la toma de decisiones agronómicas basadas en datos reales de campo.
    """)
with col2:
    st.info("💡 **Dato clave:** El dataset contiene mediciones de **pH, materia orgánica, fósforo, calcio, magnesio, potasio** y 8 micronutrientes adicionales por cada muestra de suelo.")

st.divider()

# ── 2. Descripción del Dataset ────────────────────────────────────
st.header("📊 Descripción del Dataset")

m1, m2, m3, m4 = st.columns(4)
m1.metric("📋 Registros totales", "92,738", "muestras de suelo")
m2.metric("📁 Variables",         "32",     "columnas")
m3.metric("🗺️ Departamentos",    "33",     "cubiertos")
m4.metric("🌿 Tipos de cultivo", "282",    "identificados")

st.markdown("""
El dataset incluye las siguientes categorías de variables:

- **Identificación**: Secuencial, Fecha de Análisis, Departamento, Municipio, Cultivo, Estado del cultivo.
- **Condiciones agronómicas**: Tiempo de establecimiento, Topografía, Drenaje, Riego, Fertilizantes aplicados.
- **Propiedades químicas**: pH agua:suelo, Materia orgánica, Fósforo Bray II, Azufre, Acidez intercambiable, Aluminio, Calcio, Magnesio, Potasio, Sodio, CIC, Conductividad eléctrica.
- **Micronutrientes** (métodos Olsen y Doble Ácido): Hierro, Cobre, Manganeso, Zinc, Boro.
""")

st.divider()

# ── 3. Objetivos ─────────────────────────────────────────────────
st.header("🎯 Objetivos del Proyecto")

obj_gen, obj_esp = st.columns(2)
with obj_gen:
    st.subheader("Objetivo General")
    st.markdown("""
    - Desarrollar un análisis exploratorio integral del dataset de suelos agrícolas de Colombia
      para identificar patrones de fertilidad, distribución geográfica de cultivos y calidad
      fisicoquímica del suelo como soporte a la toma de decisiones agronómicas.
    """)
with obj_esp:
    st.subheader("Objetivos Específicos")
    st.markdown("""
    - Explorar la distribución geográfica de los análisis de suelo por departamento y municipio.
    - Analizar los valores promedio de pH, materia orgánica y nutrientes por tipo de cultivo.
    - Identificar valores atípicos y datos faltantes en las propiedades químicas del suelo.
    - Comparar las condiciones de drenaje, riego y topografía entre regiones productivas.
    - Generar visualizaciones que faciliten la interpretación agronómica de los resultados.
    """)

st.divider()

# ── 4. Equipo ─────────────────────────────────────────────────────
st.header("👥 Equipo de Trabajo")

integrantes = [
    {"nombre": "Sebastián Pino",  "rol": "Líder de Analista de Datos",  "emoji": "👨‍💻"},
    {"nombre": "Jefferson Suaza", "rol": "Desarrollador de Datos",       "emoji": "👨‍🔬"},
    {"nombre": "Luisa Yepez",     "rol": "Desarrolladora de Soluciones", "emoji": "👩‍💼"},
]
cols = st.columns(len(integrantes))
for i, p in enumerate(integrantes):
    with cols[i]:
        st.markdown(f"### {p['emoji']} {p['nombre']}\n**Rol:** {p['rol']}")

st.divider()

# ── 5. Tecnologías ────────────────────────────────────────────────
st.header("🛠️ Tecnologías Utilizadas")

t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("### 🐍 Python")
    st.write("Lenguaje base para el procesamiento, limpieza y análisis del dataset de suelos.")
with t2:
    st.markdown("### 🐼 Pandas")
    st.write("Manipulación y análisis de las 92,738 filas y 32 columnas del dataset.")
with t3:
    st.markdown("### 🎈 Streamlit")
    st.write("Framework para la creación de este tablero interactivo de analítica agrícola.")

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.success("👈 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** Análisis de suelos · Colombia 2014–2024")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")