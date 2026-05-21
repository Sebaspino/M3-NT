import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Proyecto Integrador - Analítica de Datos",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo Personalizado (Opcional) ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f1; }
    .stApp { background-color: #f4f6f1 !important; color: #1b4332 !important; }
    .stApp p, .stApp span, .stApp label, .stApp li, .stApp small,
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stCaptionContainer"] *,
    h1, h2, h3, h4, h5, h6 { color: #222222 !important; }
    [data-testid="stMarkdownContainer"] strong { color: #1b4332 !important; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown * { color: #d8f3dc !important; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Título Principal ---
st.title("🚀 Proyecto Integrador: Analítica de Datos")
st.subheader("Transformando Información en Decisiones Estratégicas")

st.divider()

# --- 1. Introducción ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📖 Introducción")
    st.write("""
    Este proyecto nace de la necesidad de aplicar técnicas avanzadas de **Analítica de Datos** para resolver problemas complejos en el mundo real. 
    A través de este tablero interactivo, exploraremos cómo la ciencia de datos puede revelar patrones ocultos, optimizar procesos y predecir tendencias futuras.
    
    Nuestro enfoque se centra en la **Exploración de Datos (EDA)**, la limpieza de registros y la generación de conocimiento accionable a partir de fuentes de datos diversas.
    """)

with col2:
    st.info("💡 **Dato Curioso:** El 80% del trabajo de un analista de datos se dedica a la limpieza y preparación de la información.")

# --- 2. Objetivos ---
st.header("🎯 Objetivos del Proyecto")

obj_gen, obj_esp = st.columns(2)

with obj_gen:
    st.subheader("Objetivo General")
    st.markdown("""
    - Desarrollar un ecosistema analítico integral que permita la carga, procesamiento y análisis técnico de grandes volúmenes de datos para la toma de decisiones.
    """)

with obj_esp:
    st.subheader("Objetivos Específicos")
    st.markdown("""
    - Implementar un módulo de **Análisis Exploratorio (EDA)** adaptable a cualquier dataset CSV.
    - Fomentar el pensamiento crítico mediante actividades de "Detective de Datos".
    - Automatizar la identificación de anomalías y valores faltantes en la información.
    - Escalar el proyecto hacia modelos predictivos y visualizaciones avanzadas.
    """)

st.divider()

# --- 3. Equipo de Trabajo ---
st.header("👥 Equipo de Trabajo (Integrantes)")

# Puedes ajustar los nombres aquí
integrantes = [
    {"nombre": "Sebastián Pino", "rol": "Líder de Analista de Datos", "emoji": "👨‍💻"},
    {"nombre": "Jefferson Suaza", "rol": "Desarrollador de Datos", "emoji": "👩‍🔬"},
    {"nombre": "Luisa Yepez", "rol": "Desarrolladora de Soluciones", "emoji": "👨‍💼"},
]

cols = st.columns(len(integrantes))

for i, persona in enumerate(integrantes):
    with cols[i]:
        st.markdown(f"""
        ### {persona['emoji']} {persona['nombre']}
        **Roles:** {persona['rol']}
        """)

st.divider()

# --- 4. Tecnologías Utilizadas ---
st.header("🛠️ Tecnologías")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("### 🐍 Python")
    st.write("Lenguaje base para el procesamiento y lógica del proyecto.")

with tech_col2:
    st.markdown("### 🐼 Pandas")
    st.write("Librería líder para manipulación y análisis de estructuras de datos.")

with tech_col3:
    st.markdown("### 🎈 Streamlit")
    st.write("Framework para la creación de aplicaciones web interactivas de datos.")

# --- Pie de página ---
st.sidebar.success("👈 Usa el menú lateral para navegar entre las secciones del proyecto.")
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto Integrador de Analítica")