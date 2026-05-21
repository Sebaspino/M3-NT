import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ── FORZAR TEMA CLARO EN PLOTLY GLOBALMENTE ───────────────────────────────────
LAYOUT_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#1b4332", family="sans-serif"),
    xaxis=dict(
        showgrid=True, gridcolor="#e8ede8", linecolor="#cccccc",
        tickfont=dict(color="#333333"), title_font=dict(color="#1b4332"),
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#e8ede8", linecolor="#cccccc",
        tickfont=dict(color="#333333"), title_font=dict(color="#1b4332"),
    ),
    legend=dict(
        bgcolor="white", bordercolor="#dddddd", borderwidth=1,
        font=dict(color="#333333"),
    ),
    margin=dict(t=10, b=50, l=10, r=10),
)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Análisis de Suelos – Colombia",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS — sidebar + KPI cards (coherente con todas las páginas de suelos) ──────
st.markdown("""
<style>
    .stApp { background-color: #f4f6f1 !important; color: #1b4332 !important; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown * { color: #d8f3dc !important; }
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stSlider { color: #d8f3dc !important; }
    /* KPI cards */
    .kpi-row  { display:flex; gap:10px; margin-bottom:18px; }
    .kpi-card {
        flex:1; min-width:0; background:white; border-radius:12px;
        padding:14px 8px; text-align:center;
        box-shadow:0 2px 8px rgba(0,0,0,0.07);
        border-top:4px solid #40916c; box-sizing:border-box;
    }
    .kpi-icon  { font-size:1.3rem; line-height:1.6; color:#1b4332 !important; }
    .kpi-value { font-size:1.55rem; font-weight:700; color:#1b4332 !important; line-height:1.2; }
    .kpi-label { font-size:0.73rem; color:#555 !important; margin-top:3px; font-weight:600; }
    .kpi-sub   { font-size:0.65rem; color:#40916c !important; margin-top:2px; }

    /* Títulos de sección */
    .section-title {
        font-size:1rem; font-weight:700; color:#1b4332 !important;
        border-left:4px solid #40916c; padding-left:10px;
        margin:18px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
NUMERIC_COLS = {
    "pH (agua:suelo)":              "pH agua:suelo",
    "Materia Orgánica (%)":         "Materia organica",
    "Fósforo Bray II (mg/kg)":      "Fósforo Bray II",
    "Azufre (mg/kg)":               "Azufre Fosfato monocalcico",
    "Calcio intercambiable":        "Calcio intercambiable",
    "Magnesio intercambiable":      "Magnesio intercambiable",
    "Potasio intercambiable":       "Potasio intercambiable",
    "Conductividad Eléctrica":      "Conductividad electrica",
    "Hierro disponible (mg/kg)":    "Hierro disponible olsen",
    "Cobre disponible (mg/kg)":     "Cobre disponible",
    "Manganeso disponible (mg/kg)": "Manganeso disponible Olsen",
    "Zinc disponible (mg/kg)":      "Zinc disponible Olsen",
    "Boro disponible (mg/kg)":      "Boro disponible",
}

PH_CATS = [
    ("Muy ácido (<4.5)",     0.0,  4.5, "#d62828"),
    ("Ácido (4.5–5.5)",      4.5,  5.5, "#f4a261"),
    ("Mod. ácido (5.5–6.0)", 5.5,  6.0, "#e9c46a"),
    ("Lig. ácido (6.0–6.5)", 6.0,  6.5, "#a7c957"),
    ("Neutro (6.5–7.0)",     6.5,  7.0, "#52b788"),
    ("Alcalino (>7.0)",      7.0, 15.0, "#2d6a4f"),
]

GREENS = ["#1b4332","#2d6a4f","#40916c","#52b788","#74c69d","#95d5b2","#b7e4c7","#d8f3dc"]

# ── DATOS ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando datos…")
def load_data():
    df = pd.read_csv("data.csv", low_memory=False)
    for raw in NUMERIC_COLS.values():
        if raw in df.columns:
            df[raw] = pd.to_numeric(df[raw], errors="coerce")
    # Limpiar y filtrar valores sin información
    df["Cultivo"]      = df["Cultivo"].str.strip().fillna("Sin datos")
    df["Departamento"] = df["Departamento"].str.strip().fillna("Sin datos")
    _excluir = {"no indica", "no indicado", "sin datos", "sin información",
                "sin informacion", "nd", "n/a", "na", "", "ninguno"}
    df = df[~df["Cultivo"].str.lower().str.strip().isin(_excluir)]
    df = df[~df["Departamento"].str.lower().str.strip().isin(_excluir)]
    # Limpiar columnas categóricas de prácticas agrícolas
    for col in ["Drenaje", "Riego", "Fertilizantes aplicados"]:
        if col in df.columns:
            df[col] = df[col].str.strip()
            df[col] = df[col].where(~df[col].str.lower().isin(_excluir), other=np.nan)
    # Consolidar variantes de Riego sin sistema → "Sin riego"
    if "Riego" in df.columns:
        df["Riego"] = df["Riego"].replace({"No Tiene": "Sin riego", "No tiene": "Sin riego"})

    def cat_ph(v):
        if pd.isna(v): return "Sin datos"
        for lbl, lo, hi, _ in PH_CATS:
            if lo <= v < hi: return lbl
        return "Sin datos"

    df["Categoría pH"] = df["pH agua:suelo"].apply(cat_ph)
    df["Año"] = pd.to_datetime(
        df["Fecha de Análisis"], dayfirst=True, errors="coerce"
    ).dt.year
    return df

df_all = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌱 Filtros")
    st.markdown("---")
    top_cultivos = df_all["Cultivo"].value_counts().head(50).index.tolist()
    cultivo_sel  = st.selectbox("🌾 Cultivo", ["Todos"] + top_cultivos)
    depto_sel    = st.selectbox("📍 Departamento",
                                ["Todos"] + sorted(df_all["Departamento"].unique().tolist()))
    st.markdown("---")
    st.markdown("**📈 Variables a analizar**")
    var_x = st.selectbox("Variable principal", list(NUMERIC_COLS.keys()), index=0)
    var_y = st.selectbox("Variable secundaria (barras por rango)", list(NUMERIC_COLS.keys()), index=1)
    st.markdown("---")
    n_top = st.slider("🔢 Top N elementos (cultivos y departamentos)", 5, 20, 8)
    st.markdown("---")
    st.markdown("<small>Fuente: IGAC – Análisis Lab. Suelos Colombia</small>",
                unsafe_allow_html=True)

# ── FILTRADO ──────────────────────────────────────────────────────────────────
df = df_all.copy()
if cultivo_sel != "Todos":
    df = df[df["Cultivo"] == cultivo_sel]
if depto_sel != "Todos":
    df = df[df["Departamento"] == depto_sel]

raw_x = NUMERIC_COLS[var_x]
raw_y = NUMERIC_COLS[var_y]

# ── HELPER: aplica layout blanco a cualquier figura Plotly ────────────────────
def apply_clean_layout(fig, height=320, extra=None):
    layout = dict(LAYOUT_BASE)
    layout["height"] = height
    if extra:
        layout.update(extra)
    fig.update_layout(**layout)
    return fig

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style='color:#1b4332; font-size:1.9rem; margin-bottom:0;'>
    🌱 Dashboard de Análisis de Suelos – Colombia
</h1>
<p style='color:#6c757d; font-size:0.9rem; margin-top:4px;'>
    Cultivo: <b>{cultivo_sel}</b> &nbsp;|&nbsp;
    Departamento: <b>{depto_sel}</b> &nbsp;|&nbsp;
    <b>{len(df):,}</b> muestras
</p>
<hr style='border:1px solid #d8f3dc; margin:8px 0 16px 0;'>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
kpis = [
    ("🧪", f"{df['pH agua:suelo'].mean():.2f}",
     "pH Promedio", "óptimo: 5.5–7.0"),
    ("🌿", f"{df['Materia organica'].mean():.2f}%",
     "Materia Orgánica", "% en suelo"),
    ("🔬", f"{df['Fósforo Bray II'].mean():.1f}",
     "Fósforo (mg/kg)", "Bray II"),
    ("📍", str(df["Departamento"].nunique()),
     "Departamentos", "con datos"),
    ("🌾", str(df["Cultivo"].nunique()),
     "Cultivos", "en selección"),
]

cards_html = "<div class='kpi-row'>"
for icon, val, label, sub in kpis:
    cards_html += f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>{icon}</div>
        <div class='kpi-value'>{val}</div>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>"""
cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FILA 1 — Histograma pH  |  Boxplot cultivos
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Distribución de variables clave</div>",
            unsafe_allow_html=True)

st.markdown(f"**🌾 Cantidad de muestras por cultivo (Top {n_top})**")
_cult_cnt = (
    df["Cultivo"].value_counts()
    .head(n_top)
    .reset_index()
    .rename(columns={"Cultivo": "Cultivo", "count": "N"})
    .sort_values("N", ascending=False)
)

fig_cult = go.Figure()
fig_cult.add_trace(go.Bar(
    x=_cult_cnt["Cultivo"],
    y=_cult_cnt["N"],
    marker=dict(
        color=_cult_cnt["N"],
        colorscale=[[0, "#95d5b2"], [0.5, "#40916c"], [1, "#1b4332"]],
        showscale=False,
        line=dict(color="white", width=1.5),
    ),
    text=[f"{int(v):,}" for v in _cult_cnt["N"]],
    textposition="outside",
    textfont=dict(size=11, color="#1b4332", family="monospace"),
    hovertemplate="<b>%{x}</b><br>Muestras: %{y:,}<extra></extra>",
))
apply_clean_layout(fig_cult, height=360, extra=dict(
    showlegend=False,
    xaxis=dict(
        title="Cultivo",
        title_font=dict(color="#1b4332"),
        tickfont=dict(color="#333333", size=11),
        tickangle=-35,
        gridcolor="#e8ede8",
    ),
    yaxis=dict(
        title="N° muestras",
        title_font=dict(color="#1b4332"),
        tickfont=dict(color="#333333"),
        gridcolor="#e8ede8",
    ),
    bargap=0.25,
))
st.plotly_chart(fig_cult, use_container_width=True)
st.caption("💡 El slider 'Top N elementos' del panel izquierdo controla cuántos cultivos se muestran.")

# ══════════════════════════════════════════════════════════════════════════════
# PRÁCTICAS AGRÍCOLAS — Drenaje, Riego, Fertilizantes
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Prácticas agrícolas y su relación con el suelo</div>",
            unsafe_allow_html=True)

drain_palette = GREENS[:6]

# ── Drenaje: distribución de muestras por tipo ───────────────────────────────
st.markdown("**💧 Distribución de muestras por tipo de drenaje**")
_drain_cnt = (
    df["Drenaje"].dropna()
    .value_counts()
    .reset_index()
    .rename(columns={"Drenaje": "Tipo", "count": "N"})
    .sort_values("N", ascending=False)
)
_drain_cnt["Porcentaje"] = (_drain_cnt["N"] / _drain_cnt["N"].sum() * 100).round(1)
fig_drain = go.Figure(go.Pie(
    labels=_drain_cnt["Tipo"],
    values=_drain_cnt["N"],
    hole=0.55,
    marker=dict(
        colors=[drain_palette[i % len(drain_palette)] for i in range(len(_drain_cnt))],
        line=dict(color="white", width=3),
    ),
    textinfo="percent",
    textfont=dict(size=13, color="white"),
    hovertemplate="<b>%{label}</b><br>%{value:,} muestras<br>%{percent}<extra></extra>",
    direction="clockwise",
    sort=False,
))
fig_drain.update_layout(
    paper_bgcolor="white", plot_bgcolor="white",
    height=260,
    margin=dict(t=10, b=10, l=10, r=10),
    legend=dict(
        orientation="v",
        x=1.02, y=0.5,
        font=dict(size=12, color="#333333"),
        bgcolor="white",
        borderwidth=0,
        itemsizing="constant",
    ),
    annotations=[dict(
        text=f"<b>{int(_drain_cnt['N'].sum()):,}</b><br><span style='font-size:10px'>muestras</span>",
        x=0.5, y=0.5, font=dict(size=13, color="#1b4332"),
        showarrow=False,
    )],
)
st.plotly_chart(fig_drain, use_container_width=True)
st.caption("💡 La mayoría de suelos analizados tienen buen drenaje. Los suelos con mal drenaje son más susceptibles a compactación y pérdida de nutrientes.")


# ── Fertilizantes: top tipos más usados ──────────────────────────────────────
st.markdown("**🌿 Top 12 fertilizantes más aplicados**")
_excluir_fert = {"no indica", "no indicado", "nd", "n/a", "na", "", "no", "si", "sí",
                 "ninguno", "no ha aplicado", "no aplica", "fertilizantes químicos",
                 "produccion", "producción", "sí aplica", "si aplica"}
_fert_src = df_all if cultivo_sel == "Todos" and depto_sel == "Todos" else df
_fert_raw = _fert_src["Fertilizantes aplicados"].dropna().str.strip().str.upper()
_fert_raw = _fert_raw[~_fert_raw.str.lower().isin(_excluir_fert)]
_fert_cnt = (
    _fert_raw.value_counts()
    .head(12)
    .reset_index()
    .rename(columns={"Fertilizantes aplicados": "Fertilizante", "count": "N"})
    .sort_values("N")
)
if len(_fert_cnt) > 0:
    fig_fert = go.Figure()
    # Líneas horizontales (palito del lollipop)
    for i, row in _fert_cnt.iterrows():
        c = drain_palette[i % len(drain_palette)]
        fig_fert.add_trace(go.Scatter(
            x=[0, row["N"]], y=[row["Fertilizante"], row["Fertilizante"]],
            mode="lines",
            line=dict(color=c, width=2),
            showlegend=False,
            hoverinfo="skip",
        ))
    # Puntos + etiquetas
    for i, row in _fert_cnt.iterrows():
        c = drain_palette[i % len(drain_palette)]
        fig_fert.add_trace(go.Scatter(
            x=[row["N"]], y=[row["Fertilizante"]],
            mode="markers+text",
            marker=dict(size=16, color=c, line=dict(color="white", width=2)),
            text=[f" {int(row['N']):,}"],
            textposition="middle right",
            textfont=dict(size=10, color="#1b4332"),
            showlegend=False,
            hovertemplate=f"<b>{row['Fertilizante']}</b><br>Muestras: {int(row['N']):,}<extra></extra>",
        ))
    apply_clean_layout(fig_fert, height=max(300, len(_fert_cnt) * 38), extra=dict(
        showlegend=False,
        xaxis=dict(title="N° muestras", title_font=dict(color="#1b4332"),
                   tickfont=dict(color="#333333"), gridcolor="#e8ede8",
                   range=[0, _fert_cnt["N"].max() * 1.18]),
        yaxis=dict(tickfont=dict(color="#333333", size=10)),
        bargap=0.3,
    ))
    st.plotly_chart(fig_fert, use_container_width=True)
    st.caption("💡 Los fertilizantes balanceados (15-15-15, NPK) y la urea son los más usados. La gallinaza y vinaza representan opciones orgánicas.")
else:
    st.info("No hay datos de fertilizantes específicos para el filtro seleccionado.")

st.markdown(f"**🎯 {var_x} — Mediana e intervalo por cultivo (Top {n_top})**")
top_cult = df_all["Cultivo"].value_counts().head(n_top).index.tolist()
lol_src  = df_all[df_all["Cultivo"].isin(top_cult)][[raw_x, "Cultivo"]].dropna()
# Recortar outliers duros al p5–p95 para que el eje sea legible
p5  = lol_src[raw_x].quantile(0.05)
p95 = lol_src[raw_x].quantile(0.95)
lol_src = lol_src[(lol_src[raw_x] >= p5) & (lol_src[raw_x] <= p95)]

lol_agg = (
    lol_src.groupby("Cultivo")[raw_x]
    .agg(
        Mediana="median",
        Q1=lambda s: s.quantile(0.25),
        Q3=lambda s: s.quantile(0.75),
        N="count",
    )
    .reset_index()
    .sort_values("Mediana")
)

fig_lol = go.Figure()
for i, row in lol_agg.iterrows():
    color = GREENS[i % len(GREENS)]
    # Línea IQR (Q1 a Q3)
    fig_lol.add_trace(go.Scatter(
        x=[row["Q1"], row["Q3"]],
        y=[row["Cultivo"], row["Cultivo"]],
        mode="lines",
        line=dict(color=color, width=10),
        opacity=0.35,
        showlegend=False,
        hoverinfo="skip",
    ))
    # Punto mediana + etiqueta
    fig_lol.add_trace(go.Scatter(
        x=[row["Mediana"]],
        y=[row["Cultivo"]],
        mode="markers+text",
        marker=dict(size=14, color=color, line=dict(color="white", width=2)),
        text=[f"  {row['Mediana']:.2f}"],
        textposition="middle right",
        textfont=dict(size=10, color="#1b4332", family="monospace"),
        name=row["Cultivo"],
        showlegend=False,
        hovertemplate=(
            f"<b>{row['Cultivo']}</b><br>"
            f"Mediana: {row['Mediana']:.2f}<br>"
            f"Q1: {row['Q1']:.2f} | Q3: {row['Q3']:.2f}<br>"
            f"N: {int(row['N']):,}<extra></extra>"
        ),
    ))

apply_clean_layout(fig_lol, height=max(300, n_top * 52), extra=dict(
    showlegend=False,
    xaxis=dict(
        title=var_x, title_font=dict(color="#1b4332"),
        tickfont=dict(color="#333333"),
        gridcolor="#e8ede8", linecolor="#cccccc",
    ),
    yaxis=dict(
        tickfont=dict(color="#333333", size=11),
        gridcolor="#e8ede8", linecolor="#cccccc",
        categoryorder="array", categoryarray=lol_agg["Cultivo"].tolist(),
    ),
))
st.plotly_chart(fig_lol, use_container_width=True)
st.caption(f"💡 El punto indica la mediana; la barra gruesa muestra el rango intercuartil (Q1–Q3) del 50% central de datos.")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 2 — Scatter  |  Barras departamentos
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Relaciones entre variables y distribución geográfica</div>",
            unsafe_allow_html=True)

# ── Barras con IC: promedio de var_y por quintil de var_x ─────────────────────
st.markdown(f"**📊 Promedio de {var_y} por rango de {var_x}**")
range_df = df[[raw_x, raw_y]].dropna().copy()
try:
    range_df["Rango"] = pd.qcut(range_df[raw_x], q=5, duplicates="drop")
    range_agg = (
        range_df.groupby("Rango", observed=True)[raw_y]
        .agg(Media="mean", DE="std", N="count")
        .reset_index()
        .dropna()
    )
    range_agg["Rango"] = range_agg["Rango"].astype(str)
    range_agg["err"] = range_agg["DE"] / np.sqrt(range_agg["N"])

    fig_bar = go.Figure()
    # Área rellena con forma escalonada
    fig_bar.add_trace(go.Scatter(
        x=range_agg["Rango"],
        y=range_agg["Media"],
        mode="lines+markers+text",
        fill="tozeroy",
        fillcolor="rgba(64,145,108,0.18)",
        line=dict(color="#2d6a4f", width=2.5, shape="spline"),
        marker=dict(
            size=12,
            color=range_agg["Media"],
            colorscale=[[0, "#95d5b2"], [0.5, "#40916c"], [1, "#1b4332"]],
            line=dict(color="white", width=2),
            showscale=False,
        ),
        text=[f"{v:.2f}" for v in range_agg["Media"]],
        textposition="top center",
        textfont=dict(size=10, color="#1b4332", family="monospace"),
        error_y=dict(
            type="data", array=range_agg["err"].tolist(), visible=True,
            color="#40916c", thickness=1.5, width=5,
        ),
        hovertemplate=(
            "Rango: %{x}<br>"
            "Promedio: %{y:.2f}<extra></extra>"
        ),
    ))
    apply_clean_layout(fig_bar, height=340, extra=dict(
        showlegend=False,
        xaxis=dict(title=var_x, tickfont=dict(size=10, color="#333333"),
                   title_font=dict(color="#1b4332")),
        yaxis=dict(title=var_y, tickfont=dict(color="#333333"),
                   title_font=dict(color="#1b4332"), rangemode="tozero"),
    ))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption(f"💡 Cada barra muestra el promedio de {var_y} para un rango de {var_x}. Las líneas verticales indican el intervalo de confianza.")
except Exception:
    st.info("No hay suficientes datos para generar este gráfico con el filtro actual.")

st.markdown(f"**📍 {var_x} mediana por departamento (Top {n_top})**")
dep_df = (
    df.groupby("Departamento")[raw_x]
    .agg(Mediana="median", N="count")
    .reset_index()
    .query("N >= 10")
    .nlargest(n_top, "Mediana")
    .sort_values("Mediana")
)

fig_dep = go.Figure()
# Líneas desde 0 al punto (lollipop)
for _, row in dep_df.iterrows():
    fig_dep.add_shape(
        type="line",
        x0=dep_df["Mediana"].min() * 0.95, x1=row["Mediana"],
        y0=row["Departamento"], y1=row["Departamento"],
        line=dict(color="#d8f3dc", width=1.5),
    )
# Burbujas con tamaño proporcional a N muestras
fig_dep.add_trace(go.Scatter(
    x=dep_df["Mediana"],
    y=dep_df["Departamento"],
    mode="markers+text",
    marker=dict(
        size=dep_df["N"].clip(upper=dep_df["N"].quantile(0.9)),
        sizemode="area",
        sizeref=2.0 * dep_df["N"].max() / (28**2),
        sizemin=8,
        color=dep_df["Mediana"],
        colorscale=[[0, "#95d5b2"], [0.5, "#40916c"], [1, "#1b4332"]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Mediana", font=dict(color="#1b4332", size=10)),
            thickness=10, len=0.7,
            tickfont=dict(color="#333333", size=9),
        ),
        line=dict(color="white", width=1.5),
    ),
    text=[f"  {v:.2f}" for v in dep_df["Mediana"]],
    textposition="middle right",
    textfont=dict(size=10, color="#1b4332", family="monospace"),
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Mediana: %{x:.2f}<br>"
        "N muestras: %{marker.size:,}<extra></extra>"
    ),
    showlegend=False,
))
apply_clean_layout(fig_dep, height=340, extra=dict(
    xaxis=dict(
        title=var_x, title_font=dict(color="#1b4332"),
        tickfont=dict(color="#333333"), gridcolor="#e8ede8",
    ),
    yaxis=dict(
        tickfont=dict(color="#333333", size=11), title="",
        categoryorder="array", categoryarray=dep_df["Departamento"].tolist(),
    ),
    showlegend=False,
))
st.plotly_chart(fig_dep, use_container_width=True)
st.caption("💡 Se muestra la mediana para reducir el efecto de valores atípicos. El tamaño del punto refleja el número de muestras.")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 3 — Donut pH (Plotly)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Categorización del pH</div>",
            unsafe_allow_html=True)

st.markdown("**🍩 Categorías de acidez del suelo**")
cat_counts = df["Categoría pH"].value_counts().reset_index()
cat_counts.columns = ["Categoría", "N"]
ph_colors = {c[0]: c[3] for c in PH_CATS}
order_map  = {c[0]: i for i, c in enumerate(PH_CATS)}
cat_counts["orden"] = cat_counts["Categoría"].map(order_map).fillna(99)
cat_counts = cat_counts.sort_values("orden")

fig_don = go.Figure(go.Pie(
    labels=cat_counts["Categoría"],
    values=cat_counts["N"],
    hole=0.5,
    marker=dict(
        colors=[ph_colors.get(c, "#ccc") for c in cat_counts["Categoría"]],
        line=dict(color="white", width=2),
    ),
    textinfo="label+percent",
    textfont=dict(size=11, color="#1b4332"),
    hovertemplate="%{label}<br>%{value:,} muestras<br>%{percent}<extra></extra>",
))
apply_clean_layout(fig_don, height=310, extra=dict(
    legend=dict(
        orientation="v", x=1.02, y=0.5,
        font=dict(size=10, color="#333333"),
        bgcolor="white", borderwidth=0,
        itemsizing="constant",
    ),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
))
st.plotly_chart(fig_don, use_container_width=True)
st.caption("💡 La mayoría de suelos colombianos son ácidos. Cacao y café se adaptan bien a pH 5.0–6.5.")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 4 — Serie temporal
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Evolución temporal</div>",
            unsafe_allow_html=True)
st.markdown(f"**📅 Evolución anual de {var_x}**")

ts_src = df[["Año", raw_x]].dropna()
ts_agg = (
    ts_src.groupby("Año")[raw_x]
    .agg(Mediana="median", Media="mean", DE="std", N="count")
    .reset_index()
    .query("N >= 30 and Año >= 2005 and Año <= 2024")
)

if len(ts_agg) >= 3:
    ts_agg["upper"] = ts_agg["Media"] + ts_agg["DE"]
    ts_agg["lower"] = (ts_agg["Media"] - ts_agg["DE"]).clip(lower=0)

    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=ts_agg["Año"].tolist() + ts_agg["Año"].tolist()[::-1],
        y=ts_agg["upper"].tolist() + ts_agg["lower"].tolist()[::-1],
        fill="toself", fillcolor="rgba(64,145,108,0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="±1 Desv. Est.", hoverinfo="skip",
    ))
    fig_ts.add_trace(go.Scatter(
        x=ts_agg["Año"], y=ts_agg["Mediana"],
        mode="lines+markers+text",
        line=dict(color="#2d6a4f", width=2.5),
        marker=dict(size=7, color="#1b4332"),
        text=[f"{v:.2f}" for v in ts_agg["Mediana"]],
        textposition="top center",
        textfont=dict(size=9, color="#1b4332",
                      family="monospace"),
        name="Mediana",
    ))
    fig_ts.add_trace(go.Scatter(
        x=ts_agg["Año"], y=ts_agg["Media"],
        mode="lines",
        line=dict(color="#74c69d", width=1.5, dash="dot"),
        name="Media",
    ))
    apply_clean_layout(fig_ts, height=300, extra=dict(
        xaxis=dict(
            title="Año", tickmode="linear", dtick=1,
            tickangle=-45, tickfont=dict(color="#333333", size=10),
            title_font=dict(color="#1b4332"),
            gridcolor="#e8ede8", linecolor="#cccccc",
        ),
        yaxis=dict(
            title=var_x, tickfont=dict(color="#333333"),
            title_font=dict(color="#1b4332"),
            gridcolor="#e8ede8", linecolor="#cccccc",
        ),
        legend=dict(
            orientation="h", y=1.1, x=0.5, xanchor="center",
            font=dict(size=10, color="#333333"), bgcolor="white",
        ),
    ))
    st.plotly_chart(fig_ts, use_container_width=True)
    st.caption("💡 Banda verde = variabilidad ±1 desviación estándar. Línea sólida = mediana anual.")
else:
    st.info("No hay suficientes datos anuales para mostrar la serie temporal con el filtro actual.")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border:1px solid #d8f3dc; margin:28px 0 10px 0;'>
<p style='text-align:center; color:#adb5bd; font-size:0.75rem;'>
    🌱 Dashboard Suelos Colombia &nbsp;|&nbsp; Fuente: IGAC &nbsp;|&nbsp;
    Streamlit · Plotly · Altair · Seaborn
</p>
""", unsafe_allow_html=True)