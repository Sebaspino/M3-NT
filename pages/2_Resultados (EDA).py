import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Resultados EDA · Suelos Agrícolas",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Resultados del Análisis Exploratorio de Datos")
st.caption("Dataset: Análisis de Suelos Agrícolas · Colombia 2014–2024")

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

st.divider()

# ── Carga silenciosa del dataset ──────────────────────────────────
NUMERIC_COLS = [
    'pH agua:suelo', 'Materia organica', 'Fósforo Bray II',
    'Azufre Fosfato monocalcico', 'Acidez Intercambiable', 'Aluminio intercambiable',
    'Calcio intercambiable', 'Magnesio intercambiable', 'Potasio intercambiable',
    'Sodio intercambiable', 'capacidad de intercambio cationico', 'Conductividad electrica',
    'Hierro disponible olsen', 'Cobre disponible', 'Manganeso disponible Olsen',
    'Zinc disponible Olsen', 'Boro disponible',
]

@st.cache_data(show_spinner=False)
def load():
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

df = load()

top5_dept   = df['Departamento'].value_counts().head(5)
top5_cult   = df['Cultivo'].value_counts().head(5)
ph_med      = df['pH agua:suelo'].median()
mo_med      = df['Materia organica'].median()
ph_mean     = df['pH agua:suelo'].mean()
cic_mean    = df['capacidad de intercambio cationico'].mean()
fe_mean     = df['Hierro disponible olsen'].mean()
fos_max     = df['Fósforo Bray II'].max()
acid_pct    = round(df['Acidez Intercambiable'].isnull().mean() * 100, 1)
da_pct      = round(df['Hierro disponible doble acido'].isnull().mean() * 100 if 'Hierro disponible doble acido' in df.columns else 94.9, 1)

# ── 1. Identificación y Contexto ─────────────────────────────────
st.header("🔍 1. Identificación y Contexto del Dataset")
st.info(f"""
El dataset contiene **{df.shape[0]:,} registros** de análisis fisicoquímicos de suelos agrícolas en Colombia,
recolectados entre **2014 y 2024**. Cada fila representa una muestra de suelo tomada en campo,
con **{df.shape[1]} variables** que describen tanto el contexto del lote (cultivo, ubicación, topografía, riego)
como las propiedades químicas del suelo (pH, materia orgánica, macronutrientes y micronutrientes).

Su propósito es **caracterizar la fertilidad del suelo** y apoyar las decisiones agronómicas de fertilización
en cultivos de importancia nacional como cacao, café, aguacate y caña panelera.
""")

st.divider()

# ── 2. Distribución Geográfica y por Cultivo ─────────────────────
st.header("🗺️ 2. Distribución Geográfica y por Cultivo")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 Departamentos")
    dept_df = top5_dept.reset_index()
    dept_df.columns = ["Departamento", "Muestras"]
    dept_df["% del total"] = (dept_df["Muestras"] / len(df) * 100).round(1).astype(str) + "%"
    st.dataframe(dept_df.set_index("Departamento"), use_container_width=True)

with col2:
    st.subheader("Top 5 Cultivos")
    cult_df = top5_cult.reset_index()
    cult_df.columns = ["Cultivo", "Muestras"]
    cult_df["% del total"] = (cult_df["Muestras"] / len(df) * 100).round(1).astype(str) + "%"
    st.dataframe(cult_df.set_index("Cultivo"), use_container_width=True)

st.info(f"""
**{top5_dept.index[0]}** es el departamento con mayor número de muestras ({top5_dept.iloc[0]:,}, el {top5_dept.iloc[0]/len(df)*100:.1f}% del total),
seguido por {top5_dept.index[1]} y {top5_dept.index[2]}.
El cultivo más analizado es **{top5_cult.index[0]}** ({top5_cult.iloc[0]:,} muestras), lo que refleja la
prioridad del programa nacional de cacaoticultura. La distribución geográfica desigual puede indicar
menor cobertura del servicio de análisis de suelos en algunas regiones del país.
""")

st.divider()

# ── 3. Calidad de los Datos ───────────────────────────────────────
st.header("❗ 3. Calidad de los Datos y Valores Especiales")

cal_data = {
    "Variable": [
        "pH agua:suelo", "Materia Orgánica", "Fósforo Bray II",
        "Acidez / Aluminio intercambiable", "Sodio intercambiable",
        "Cobre disponible", "Zinc disponible Olsen",
        "Micronutrientes doble ácido (Fe, Cu, Mn, Zn)"
    ],
    "Faltantes (%)": ["0.0%", "0.1%", "16.2%", "~48.7%", "~48.3%", "31.6%", "41.6%", ">94.9%"],
    "Causa": [
        "Medición estándar — casi siempre completa",
        "Medición estándar — casi siempre completa",
        "No siempre se solicita en análisis básicos",
        "Solo se mide en suelos ácidos (pH < 5.5)",
        "Solo se solicita cuando hay sospecha de salinidad",
        "No incluido en todos los paquetes de análisis",
        "No incluido en todos los paquetes de análisis",
        "Metodología alternativa poco usada en Colombia",
    ]
}
st.dataframe(pd.DataFrame(cal_data).set_index("Variable"), use_container_width=True)

st.warning("""
**Valores especiales encontrados:** el archivo original contiene texto como **'ND'** (No Determinado)
y **'<0.09'** (por debajo del límite de detección) en columnas numéricas.
Estos fueron convertidos a valores nulos (NaN) durante la limpieza para permitir el análisis estadístico.
Las columnas de micronutrientes por **doble ácido** se deben excluir del análisis principal por su altísimo porcentaje de faltantes (>94%).
""")

st.divider()

# ── 4. Hallazgos Estadísticos Clave ──────────────────────────────
st.header("📈 4. Hallazgos Estadísticos Clave del Suelo")

stats_show = [
    'pH agua:suelo', 'Materia organica', 'Fósforo Bray II',
    'Calcio intercambiable', 'Magnesio intercambiable',
    'capacidad de intercambio cationico', 'Hierro disponible olsen',
    'Boro disponible',
]
labels = {
    'pH agua:suelo':                      'pH (agua:suelo)',
    'Materia organica':                   'Materia Orgánica (%)',
    'Fósforo Bray II':                    'Fósforo Bray II (mg/kg)',
    'Calcio intercambiable':              'Calcio intercambiable (cmol/kg)',
    'Magnesio intercambiable':            'Magnesio intercambiable (cmol/kg)',
    'capacidad de intercambio cationico': 'CIC (cmol/kg)',
    'Hierro disponible olsen':            'Hierro disponible (mg/kg)',
    'Boro disponible':                    'Boro disponible (mg/kg)',
}
present = [c for c in stats_show if c in df.columns]
stats = df[present].agg([
    'count', 'mean', 'std', 'min',
    lambda x: x.quantile(0.25),
    'median',
    lambda x: x.quantile(0.75),
    'max'
]).T
stats.columns = ['N muestras', 'Media', 'Desv. Est.', 'Mínimo', 'Q1', 'Mediana', 'Q3', 'Máximo']
stats.index = [labels.get(c, c) for c in present]
stats['N muestras'] = stats['N muestras'].astype(int)
st.dataframe(stats.round(3), use_container_width=True)

st.info(f"""
- **pH medio de {ph_mean:.2f}** → suelos predominantemente ácidos. El 50% central de las muestras tiene pH entre 4.96 y 6.26.
- **Materia orgánica mediana de {mo_med:.2f}%** → fertilidad natural media; alta variabilidad entre regiones.
- **CIC promedio de {cic_mean:.1f} cmol/kg** → capacidad media-baja de retener nutrientes en el suelo.
- **Hierro disponible promedio de {fe_mean:.0f} mg/kg** → valores elevados típicos de suelos ácidos tropicales.
- **Fósforo Bray II** presenta alta dispersión (máximo {fos_max:,.0f} mg/kg), lo que indica tanto suelos con deficiencia como con acumulación por sobrefertilización.
""")

st.divider()

# ── 5. Conclusión ─────────────────────────────────────────────────
st.header("💡 5. Conclusión Final y Recomendaciones")
st.success(f"""
El dataset de suelos agrícolas de Colombia (2014–2024) revela que la mayoría de los suelos analizados son
**ácidos** (pH medio ~{ph_mean:.1f}), con **fertilidad media-baja** según la CIC, y con una distribución
heterogénea de nutrientes entre regiones y cultivos.

Los principales retos de calidad son los valores 'ND' en micronutrientes y la ausencia de Acidez/Aluminio
en suelos neutros. Las columnas de metodología doble ácido deben descartarse del análisis por falta de datos.

**Se recomienda como próximos pasos:**
- Analizar la correlación entre pH y Aluminio intercambiable para mapear zonas con toxicidad.
- Comparar los niveles de nutrientes por cultivo para generar recomendaciones de fertilización específicas.
- Construir un índice de fertilidad del suelo por departamento usando pH, MO y CIC como variables principales.
""")

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.write("© 2026 - Proyecto Integrador · Análisis de Suelos Colombia")