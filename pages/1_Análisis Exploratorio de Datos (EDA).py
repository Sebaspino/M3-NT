import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="EDA · Suelos Agrícolas Colombia", page_icon="🔍", layout="wide")

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

st.title("🧩 Actividad: ¿De qué se tratan estos datos?")
st.markdown("""
### Objetivo de la Actividad
Tu misión es actuar como un **detective de datos** especializado en suelos agrícolas.
A partir de las tablas y estadísticas que verás a continuación, debes deducir el contexto,
el origen y el propósito de este conjunto de datos de análisis fisicoquímicos de suelos en Colombia.
""")

# --- Barra Lateral con Instrucciones ---
with st.sidebar:
    st.warning("⚠️ **Prohibido usar gráficos**. El reto es entender los datos solo con números y texto.")
    st.markdown("---")
    st.markdown("**Contexto del dataset:** Análisis de suelos agrícolas · Colombia · 2014–2024")

# ─────────────────────────────────────────────────────────────────
# CARGA Y LIMPIEZA — sin UI, silenciosa
# ─────────────────────────────────────────────────────────────────
NUMERIC_COLS = [
    'pH agua:suelo', 'Materia organica', 'Fósforo Bray II',
    'Azufre Fosfato monocalcico', 'Acidez Intercambiable', 'Aluminio intercambiable',
    'Calcio intercambiable', 'Magnesio intercambiable', 'Potasio intercambiable',
    'Sodio intercambiable', 'capacidad de intercambio cationico', 'Conductividad electrica',
    'Hierro disponible olsen', 'Cobre disponible', 'Manganeso disponible Olsen',
    'Zinc disponible Olsen', 'Boro disponible',
    'Hierro disponible doble acido', 'Cobre disponible doble acido',
    'Manganeso disponible doble acido', 'Zinc disponible doble \xa0acido',
]

CAT_COLS = [
    'Fecha de Análisis', 'Departamento', 'Municipio', 'Cultivo', 'Estado',
    'Tiempo de establecimiento', 'Topografia', 'Drenaje', 'Riego', 'Fertilizantes aplicados',
]

STAT_LABELS = {
    'pH agua:suelo':                    'pH (agua:suelo)',
    'Materia organica':                 'Materia Orgánica (%)',
    'Fósforo Bray II':                  'Fósforo Bray II (mg/kg)',
    'Azufre Fosfato monocalcico':       'Azufre (mg/kg)',
    'Acidez Intercambiable':            'Acidez Intercambiable (cmol/kg)',
    'Aluminio intercambiable':          'Aluminio intercambiable (cmol/kg)',
    'Calcio intercambiable':            'Calcio intercambiable (cmol/kg)',
    'Magnesio intercambiable':          'Magnesio intercambiable (cmol/kg)',
    'Potasio intercambiable':           'Potasio intercambiable (cmol/kg)',
    'Sodio intercambiable':             'Sodio intercambiable (cmol/kg)',
    'capacidad de intercambio cationico': 'CIC (cmol/kg)',
    'Conductividad electrica':          'Conductividad Eléctrica (dS/m)',
    'Hierro disponible olsen':          'Hierro disponible (mg/kg)',
    'Cobre disponible':                 'Cobre disponible (mg/kg)',
    'Manganeso disponible Olsen':       'Manganeso disponible (mg/kg)',
    'Zinc disponible Olsen':            'Zinc disponible (mg/kg)',
    'Boro disponible':                  'Boro disponible (mg/kg)',
    'Hierro disponible doble acido':    'Fe doble ácido (mg/kg)',
    'Cobre disponible doble acido':     'Cu doble ácido (mg/kg)',
    'Manganeso disponible doble acido': 'Mn doble ácido (mg/kg)',
    'Zinc disponible doble \xa0acido':  'Zn doble ácido (mg/kg)',
}

@st.cache_data(show_spinner="Cargando dataset de suelos...")
def load_and_clean():
    df = pd.read_csv("data.csv", low_memory=False)
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # Limpieza coherente con las demás páginas
    _excluir = {"no indica", "no indicado", "sin datos", "sin información",
                "sin informacion", "nd", "n/a", "na", "", "ninguno"}
    df["Departamento"] = df["Departamento"].str.strip().fillna("Sin datos")
    df["Cultivo"]      = df["Cultivo"].str.strip().fillna("Sin datos")
    df = df[~df["Departamento"].str.lower().isin(_excluir)]
    df = df[~df["Cultivo"].str.lower().isin(_excluir)]
    return df

df = load_and_clean()

# ─────────────────────────────────────────────────────────────────
# PASO 1 — Primer Impacto
# ─────────────────────────────────────────────────────────────────
st.header("Step 1: 🔍 Primer Impacto (Dataset Preview)")
st.markdown("Observa las primeras filas. ¿Qué conceptos o palabras clave se repiten?")
st.dataframe(df.head(10))

with st.expander("💡 ¿Cómo interpretar este paso? — Contexto Suelos"):
    st.write("""
    - **Departamento / Municipio:** Indican la ubicación geográfica de la muestra en Colombia.
    - **Cultivo:** El tipo de planta sembrada en el lote donde se tomó la muestra (Cacao, Café, Aguacate, etc.).
    - **pH agua:suelo:** Indica la acidez del suelo. Valores menores a 5.5 son ácidos, entre 6 y 7 son óptimos para la mayoría de cultivos.
    - **Materia orgánica:** Porcentaje de materia orgánica. Valores bajos (< 2%) indican suelos pobres.
    - **Fósforo, Calcio, Magnesio, Potasio:** Son macronutrientes esenciales para el crecimiento vegetal.
    - **Hierro, Cobre, Zinc, Boro, Manganeso:** Micronutrientes que en exceso o déficit afectan la producción.
    """)

# ─────────────────────────────────────────────────────────────────
# PASO 2 — La Estructura
# ─────────────────────────────────────────────────────────────────
st.header("Step 2: 🏗️ La Estructura")
col1, col2 = st.columns(2)

with col1:
    st.subheader("¿Qué tan grande es?")
    st.write(f"Filas (muestras de suelo): **{df.shape[0]:,}**")
    st.write(f"Columnas (variables medidas): **{df.shape[1]}**")
    st.write(f"Período de análisis: **2014 – 2024**")
    st.write(f"Departamentos con datos: **{df['Departamento'].nunique()}**")
    st.write(f"Municipios registrados: **{df['Municipio'].nunique()}**")
    st.write(f"Tipos de cultivo: **{df['Cultivo'].nunique()}**")

with col2:
    st.subheader("¿Qué tipos de datos hay?")
    # Construir tabla de tipos correcta después de la conversión
    tipo_map = {}
    for col in df.columns:
        if col in NUMERIC_COLS:
            tipo_map[col] = "float64 (numérico)"
        elif col == 'Secuencial':
            tipo_map[col] = "int64 (identificador)"
        elif col in CAT_COLS:
            tipo_map[col] = "object (categórico / texto)"
        else:
            tipo_map[col] = str(df[col].dtype)
    tipos_df = pd.DataFrame(
        list(tipo_map.items()), columns=["Columna", "Tipo de dato"]
    ).set_index("Columna")
    st.dataframe(tipos_df, use_container_width=True)

with st.expander("💡 ¿Cómo interpretar la estructura? — Contexto Suelos"):
    st.write("""
    - **92,738 filas:** Cada fila es una muestra de suelo individual tomada en campo. Es un dataset muy representativo del territorio colombiano.
    - **{df.shape[1]} columnas:** 11 variables de contexto (ubicación, cultivo, condiciones del lote) y 21 variables de análisis químico.
    - **object (categórico/texto):** Columnas como Departamento, Municipio, Cultivo, Drenaje y Riego son categóricas.
    - **float64 (numérico):** Las propiedades químicas (pH, nutrientes, micronutrientes) son valores decimales continuos.
    - **Nota:** Estas columnas fueron originalmente cargadas como texto porque contienen valores especiales como 'ND' o '<0.09', que fueron convertidos a NaN durante la limpieza.
    """)

# ─────────────────────────────────────────────────────────────────
# PASO 3 — Calidad y Vacíos
# ─────────────────────────────────────────────────────────────────
st.header("Step 3: ❗ Calidad y Vacíos")

# Calcular nulos reales en columnas numéricas (resultado de convertir ND / <0.09)
num_present = [c for c in NUMERIC_COLS if c in df.columns]
null_counts = df[num_present].isnull().sum()
null_pct    = (null_counts / len(df) * 100).round(1)

calidad_df = pd.DataFrame({
    "Variable": [STAT_LABELS.get(c, c) for c in num_present],
    "Valores faltantes": null_counts.values,
    "% del total": null_pct.values,
    "Causa probable": [
        "Muy completo — casi todos los laboratorios miden pH",
        "Muy completo",
        "Algunos lotes no solicitaron análisis de fósforo",
        "Pequeño porcentaje sin medición de azufre",
        "Solo se mide en suelos ácidos (~48% de los casos)",
        "Ídem — va de la mano con Acidez Intercambiable",
        "Algunos análisis básicos omiten calcio",
        "Ídem magnesio",
        "Aprox. 16% sin análisis de potasio",
        "Solo se mide en suelos con problemas de salinidad",
        "Muy completo — CIC se calcula siempre",
        "Muy completo — conductividad estándar",
        "Aprox. 8% sin hierro olsen",
        "Aprox. 32% sin cobre — no siempre se solicita",
        "Aprox. 14% sin manganeso",
        "Aprox. 42% sin zinc olsen",
        "Muy completo — boro es parte del análisis estándar",
        "~95% ND — metodología doble ácido poco usada",
        "~96% ND — metodología doble ácido poco usada",
        "~95% ND — metodología doble ácido poco usada",
        "~100% ND — prácticamente sin datos",
    ]
}).set_index("Variable")

st.dataframe(calidad_df, use_container_width=True)
st.caption("Los valores 'ND' (No Determinado) y '<0.09' del archivo original fueron convertidos a NaN durante la carga.")

col_q1, col_q2 = st.columns(2)
with col_q1:
    st.success(f"✅ Columnas contextuales (texto): solo **3 nulos** en todo el dataset.")
with col_q2:
    st.warning("⚠️ Los micronutrientes por **doble ácido** tienen >94% de datos faltantes — excluirlos del análisis principal.")

with st.expander("💡 ¿Qué significan los datos faltantes? — Contexto Suelos"):
    st.write("""
    - **'ND' (No Determinado):** El laboratorio no realizó esa medición, común en micronutrientes.
    - **'<0.09':** Valor por debajo del límite de detección del equipo. Tratado como NaN (no como cero).
    - **Acidez / Aluminio intercambiable (48.7% faltante):** Solo se analizan en suelos ácidos (pH < 5.5), por eso están ausentes en suelos neutros o básicos.
    - **Sodio intercambiable (48.3% faltante):** Solo se solicita cuando se sospecha de salinidad del suelo.
    - **Micronutrientes doble ácido (>94% faltante):** Esta es una metodología alternativa al método Olsen, poco utilizada en Colombia.
    """)

# ─────────────────────────────────────────────────────────────────
# PASO 4 — Estadísticas (tabla descriptiva real)
# ─────────────────────────────────────────────────────────────────
st.header("Step 4: 📈 El Corazón de los Datos (Estadísticas)")

tab1, tab2 = st.tabs(["📊 Números — Propiedades Fisicoquímicas", "🔠 Categorías — Contexto Agrícola"])

with tab1:
    st.markdown("**Resumen de variables fisicoquímicas clave**")
    st.caption("Valores calculados sobre datos numéricos válidos (tras conversión de ND y <0.09 a NaN).")

    ph_mean_eda   = df['pH agua:suelo'].mean()
    mo_mean_eda   = df['Materia organica'].mean()
    cic_mean_eda  = df['capacidad de intercambio cationico'].mean() if 'capacidad de intercambio cationico' in df.columns else None
    fe_mean_eda   = df['Hierro disponible olsen'].mean() if 'Hierro disponible olsen' in df.columns else None

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("pH promedio",          f"{ph_mean_eda:.2f}",  "ácido < 5.5")
    m2.metric("Materia Orgánica (%)", f"{mo_mean_eda:.2f}",  "media: aceptable")
    if cic_mean_eda:
        m3.metric("CIC (cmol/kg)",    f"{cic_mean_eda:.1f}", "fertilidad media-baja")
    if fe_mean_eda:
        m4.metric("Hierro (mg/kg)",   f"{fe_mean_eda:.0f}",  "elevado en suelos ácidos")

    st.info("📊 La tabla estadística completa (todas las variables) está disponible en **📊 Gráficos de Laboratorio → Resumen estadístico** en el menú lateral.")

    with st.expander("📊 Guía de Estadísticas Numéricas — Suelos"):
        st.write("""
        - **pH (media ~5.7):** La mayoría de suelos colombianos son ácidos. Un pH bajo (<5.0) indica posible toxicidad por aluminio.
        - **Materia orgánica (media ~4.4%):** Promedio aceptable, pero la alta desviación estándar (4.6) indica suelos muy heterogéneos.
        - **Fósforo Bray II (media ~33 mg/kg):** Alta dispersión (std 79). Algunos lotes con acumulación extrema (máx 3015 mg/kg).
        - **Calcio y Magnesio intercambiable:** Los cationes más importantes para la estructura del suelo.
        - **CIC media ~11.3 cmol/kg:** Indica suelos de fertilidad media-baja en general.
        - **Hierro disponible (media ~244 mg/kg):** Valores muy altos — el hierro libre es abundante en suelos ácidos colombianos.
        - **Min / Max extremos:** Los máximos en Fe, Mn o Zn pueden indicar toxicidad por metales en algunos lotes.
        """)

with tab2:
    cat_present = [c for c in CAT_COLS if c in df.columns]
    cat_desc = df[cat_present].describe()
    if not cat_desc.empty:
        st.write("**Resumen de las columnas categóricas:**")
        st.dataframe(cat_desc, use_container_width=True)

        with st.expander("🔠 Guía de Estadísticas Categóricas — Suelos"):
            st.write("""
            - **Departamento (top = Cundinamarca):** Con 14,016 muestras (15% del total), es la región más analizada.
            - **Cultivo (moda = Cacao):** 11,104 muestras, refleja la prioridad del programa de cacaoticultura en Colombia.
            - **Drenaje:** La categoría más frecuente indica la condición predominante de drenaje del país.
            - **Riego (top = No Tiene):** La mayoría de la agricultura colombiana analizada es de secano (depende de lluvia).
            - **Estado (top = Establecido):** La mayor parte de los cultivos ya estaban plantados al momento del análisis.
            """)
    else:
        st.info("No se detectaron columnas categóricas.")

# ─────────────────────────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────────────────────────
st.header("📝 Resumen de Hallazgos")

top_dept    = df['Departamento'].value_counts().index[0]
top_cultivo = df['Cultivo'].value_counts().index[0]
num_cols_count = len([c for c in NUMERIC_COLS if c in df.columns])
cat_cols_count = len([c for c in CAT_COLS if c in df.columns])

st.markdown(f"""
### 🕵️ Informe del Detective de Suelos

Basado en tu investigación, aquí hay una síntesis de lo encontrado:

*   **Volumen**: Estás manejando **{df.shape[0]:,} muestras de suelo**, lo que permite una visión **nacional** del estado de los suelos agrícolas colombianos.
*   **Cobertura geográfica**: El dataset abarca **{df['Departamento'].nunique()} departamentos** y **{df['Municipio'].nunique()} municipios**. El más representado es **{top_dept}**.
*   **Cultivo dominante**: El cultivo con más análisis es **{top_cultivo}**, seguido de pastos y aguacate.
*   **Variables**: El dataset contiene **{cat_cols_count} variables de contexto** (ubicación, cultivo, condiciones) y **{num_cols_count} variables numéricas** (propiedades fisicoquímicas del suelo).
*   **Calidad de datos**: Las columnas de micronutrientes por **doble ácido** tienen >94% de datos faltantes (ND). Los métodos Olsen son los más completos. La **Acidez y Aluminio intercambiable** solo se miden en suelos ácidos (~48% del dataset).

**¿Lograste identificar que se trata de un dataset de análisis de suelos agrícolas de Colombia (2014–2024)?**
""")