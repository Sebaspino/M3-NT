import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import warnings
warnings.filterwarnings("ignore")

BASE_URL = "http://localhost:8080"

# ── PALETA SERENITYLAB ────────────────────────────────────────────────────────
# Paleta fiel al sitio: rosa cálido, no fucsia saturado
S_DARK    = "#880e4f"   # vino rosa — titulares del sitio
S_MED     = "#ad1457"   # rosa medio — acentos
S_BASE    = "#e91e8c"   # rosa vivo — logo / links activos
S_LIGHT   = "#f48fb1"   # rosa claro — hover / bordes
S_PALE    = "#fce4ec"   # rosa pálido — fondos de sección
S_BG      = "rgba(252, 228, 236, 0.45)"  # fondo suave
S_BORDER  = "rgba(244, 143, 177, 0.35)"  # borde sutil

PINKS = [S_DARK, S_MED, S_BASE, S_LIGHT, S_PALE,
         "#fce4ec", "#fdf2f8", "#fff8fb"]

LAYOUT_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color=S_DARK, family="sans-serif"),
    xaxis=dict(
        showgrid=True, gridcolor="#fce7f3", linecolor="#f9a8d4",
        tickfont=dict(color="#333333"), title_font=dict(color=S_DARK),
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#fce7f3", linecolor="#f9a8d4",
        tickfont=dict(color="#333333"), title_font=dict(color=S_DARK),
    ),
    legend=dict(
        bgcolor="white", bordercolor="#fbcfe8", borderwidth=1,
        font=dict(color="#333333"),
    ),
    margin=dict(t=10, b=50, l=10, r=10),
)

ESTADO_COLORES = {
    "Pendiente":  "#fbbf24",
    "Confirmada": "#34d399",
    "Cancelada":  "#f87171",
    "Realizada":  S_MED,
    "No Asistió": "#fb923c",
}

DIAS_ES = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SerenityLab — Analítica",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* ── Fondo principal blanco ── */
    .stApp {{
        background-color: #ffffff !important;
        color: {S_DARK} !important;
    }}
    .stApp p, .stApp span, .stApp label, .stApp li, .stApp small,
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stCaptionContainer"] *,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
    .stCaption, .stCaption *, h1, h2, h3, h4, h5, h6 {{
        color: #222222 !important;
    }}
    [data-testid="stMarkdownContainer"] strong {{ color: {S_DARK} !important; }}
    [data-testid="stDataFrame"] * {{ color: #222222 !important; }}

    /* ── Sidebar: rosa muy claro, como el sitio ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #f8bbd0 0%, #fce4ec 60%, #fff8fb 100%) !important;
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown * {{ color: {S_DARK} !important; }}

    /* ── Ocultar botón nativo de Streamlit (lo reemplazamos con HTML) ── */
    [data-testid="stSidebar"] .stButton {{ display: none !important; }}

    /* ── Botón HTML personalizado ── */
    .refresh-btn {{
        display: block;
        width: 100%;
        padding: 9px 0;
        background-color: #ffffff;
        color: {S_DARK} !important;
        border: 1.5px solid {S_LIGHT};
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        margin: 4px 0 12px 0;
        text-decoration: none;
        transition: background 0.18s;
    }}
    .refresh-btn:hover {{
        background-color: {S_PALE};
        border-color: {S_MED};
    }}

    /* ── KPI cards ── */
    .kpi-row  {{ display:flex; gap:10px; margin-bottom:18px; }}
    .kpi-card {{
        flex:1; min-width:0; background:white; border-radius:12px;
        padding:14px 8px; text-align:center;
        box-shadow:0 2px 10px rgba(136,14,79,0.08);
        border: 1px solid {S_BORDER};
        border-top: 4px solid {S_BASE};
        box-sizing:border-box;
    }}
    .kpi-icon  {{ font-size:1.3rem; line-height:1.6; }}
    .kpi-value {{ font-size:1.55rem; font-weight:700; color:{S_DARK} !important; line-height:1.2; }}
    .kpi-label {{ font-size:0.73rem; color:#555 !important; margin-top:3px; font-weight:600; }}
    .kpi-sub   {{ font-size:0.65rem; color:{S_MED} !important; margin-top:2px; }}

    /* ── Títulos de sección ── */
    .section-title {{
        font-size:1rem; font-weight:700; color:{S_DARK} !important;
        border-left:4px solid {S_BASE};
        background: {S_BG}; padding: 8px 10px;
        border-radius: 0 6px 6px 0; margin:18px 0 10px 0;
    }}
    iframe {{ background: white !important; }}
</style>
""", unsafe_allow_html=True)


# ── HELPER ────────────────────────────────────────────────────────────────────
def apply_clean_layout(fig, height=320, extra=None):
    layout = dict(LAYOUT_BASE)
    layout["height"] = height
    if extra:
        layout.update(extra)
    fig.update_layout(**layout)
    return fig


# ── CARGA DE DATOS ────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner="Consultando API…")
def fetch(endpoint):
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", timeout=8)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return "connection_error"
    except Exception:
        return None


@st.cache_data(ttl=60, show_spinner="Cargando datos de SerenityLab…")
def load_all():
    return (
        fetch("/citas/"),
        fetch("/estudiantes/"),
        fetch("/psicologos/"),
        fetch("/estadoscitas/"),
    )


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 SerenityLab")
    st.markdown("---")
    # Botón nativo oculto (necesario para el rerun via CSS display:none)
    _refresh = st.button("_refresh_trigger", key="refresh_hidden")
    if _refresh:
        st.cache_data.clear()
        st.rerun()
    # Botón HTML visible que simula click en el oculto
    st.markdown("""
    <a class='refresh-btn' onclick="
        const btns = window.parent.document.querySelectorAll('button');
        for(const b of btns){ if(b.innerText.includes('_refresh_trigger')){ b.click(); break; } }
    ">🔄 Actualizar datos</a>
    """, unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style='color:{S_DARK}; font-size:1.9rem; margin-bottom:0;'>
    🧠 SerenityLab — Analítica de Citas
</h1>
<p style='color:#9d174d; font-size:0.9rem; margin-top:4px;'>
    Métricas operativas · Sistema de gestión de citas psicológicas
</p>
<hr style='border:1px solid {S_PALE}; margin:8px 0 16px 0;'>
""", unsafe_allow_html=True)


# ── FETCH ─────────────────────────────────────────────────────────────────────
citas_raw, estudiantes_raw, psicologos_raw, estados_raw = load_all()

if citas_raw == "connection_error":
    st.error(
        "**No se puede conectar al backend** (`http://localhost:8080`).\n\n"
        "Asegúrate de que el servidor Spring Boot esté corriendo y vuelve a intentarlo."
    )
    st.stop()

if not citas_raw or not isinstance(citas_raw, list):
    st.warning("El endpoint `/citas/` no retornó datos. Verifica que el backend esté inicializado.")
    st.stop()


# ── DATAFRAMES ────────────────────────────────────────────────────────────────
df_citas = pd.DataFrame(citas_raw)
df_citas["fechaCita"] = pd.to_datetime(df_citas["fechaCita"], errors="coerce")
df_citas["estadoCitaId"] = df_citas["estadoCitaId"].astype(str)

ESTADO_MAP = {"1":"Pendiente","2":"Confirmada","3":"Cancelada","4":"Realizada","5":"No Asistió"}
if isinstance(estados_raw, list) and estados_raw:
    ESTADO_MAP = {str(e["estadoId"]): e["estado"] for e in estados_raw}
df_citas["estado"] = df_citas["estadoCitaId"].map(ESTADO_MAP).fillna("Desconocido")

df_psi = pd.DataFrame(psicologos_raw if isinstance(psicologos_raw, list) else [])
if not df_psi.empty:
    df_psi["nombreCompleto"] = df_psi["nombre"] + " " + df_psi["apellido"]
    df_psi = df_psi[["psicologoId","nombreCompleto","especialidad","estado"]]

df_est = pd.DataFrame(estudiantes_raw if isinstance(estudiantes_raw, list) else [])
if not df_est.empty:
    df_est["nombreCompleto"] = df_est["nombre"] + " " + df_est["apellido"]

if not df_psi.empty:
    df_citas = df_citas.merge(
        df_psi[["psicologoId","nombreCompleto","especialidad"]],
        on="psicologoId", how="left"
    )
    df_citas["nombrePsicologo"] = df_citas["nombreCompleto"].fillna(df_citas["psicologoId"])
else:
    df_citas["nombrePsicologo"] = df_citas["psicologoId"]


# ── KPI CARDS ─────────────────────────────────────────────────────────────────
total_citas = len(df_citas)
realizadas  = (df_citas["estado"] == "Realizada").sum()
canceladas  = (df_citas["estado"] == "Cancelada").sum()
completadas = realizadas + (df_citas["estado"] == "No Asistió").sum()
tasa_asist  = f"{realizadas/completadas*100:.1f}%" if completadas > 0 else "–"
tasa_cancel = f"{canceladas/total_citas*100:.1f}%" if total_citas > 0 else "–"
psi_activos = (df_psi["estado"] == "activo").sum() if not df_psi.empty else "–"
est_activos = (df_est["estado"] == "activo").sum() if not df_est.empty else "–"

kpis = [
    ("📅", f"{total_citas:,}", "Total citas",         "registradas"),
    ("✅", tasa_asist,         "Tasa de asistencia",  "realizadas / completadas"),
    ("❌", tasa_cancel,        "Tasa de cancelación", "sobre el total"),
    ("🧑‍⚕️", str(psi_activos), "Psicólogos activos",  "en sistema"),
    ("🎓", str(est_activos),   "Estudiantes activos", "en sistema"),
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
# SECCIÓN 1 — Distribución de estados
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Distribución de citas por estado</div>",
            unsafe_allow_html=True)

estado_cnt = df_citas["estado"].value_counts().reset_index()
estado_cnt.columns = ["Estado","N"]
colors_donut = [ESTADO_COLORES.get(e,"#adb5bd") for e in estado_cnt["Estado"]]

fig_don = go.Figure(go.Pie(
    labels=estado_cnt["Estado"],
    values=estado_cnt["N"],
    hole=0.55,
    marker=dict(colors=colors_donut, line=dict(color="white", width=3)),
    textinfo="percent",
    textfont=dict(size=13, color="white"),
    hovertemplate="<b>%{label}</b><br>%{value:,} citas<br>%{percent}<extra></extra>",
    direction="clockwise",
    sort=False,
))
fig_don.update_layout(
    paper_bgcolor="white", plot_bgcolor="white",
    height=300,
    margin=dict(t=10, b=10, l=10, r=10),
    legend=dict(orientation="v", x=1.02, y=0.5,
                font=dict(size=12, color="#333333"),
                bgcolor="white", borderwidth=0),
    annotations=[dict(
        text=f"<b>{total_citas:,}</b><br><span style='font-size:10px'>citas</span>",
        x=0.5, y=0.5, font=dict(size=13, color=S_DARK), showarrow=False,
    )],
)
st.plotly_chart(fig_don, use_container_width=True)
st.caption("💡 Las citas canceladas y no asistidas representan pérdida de disponibilidad del psicólogo.")


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Carga de trabajo por psicólogo
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Carga de trabajo por psicólogo</div>",
            unsafe_allow_html=True)

st.markdown("**🧑‍⚕️ Total de citas por psicólogo**")
psi_cnt = (
    df_citas.groupby("nombrePsicologo")
    .agg(Total=("citaId","count"),
         Realizadas=("estado", lambda s: (s=="Realizada").sum()),
         Canceladas=("estado", lambda s: (s=="Cancelada").sum()))
    .reset_index()
    .sort_values("Total", ascending=False)
)

fig_psi = go.Figure()
fig_psi.add_trace(go.Bar(
    x=psi_cnt["nombrePsicologo"],
    y=psi_cnt["Total"],
    marker=dict(
        color=psi_cnt["Total"],
        colorscale=[[0, S_PALE],[0.5, S_BASE],[1, S_DARK]],
        showscale=False,
        line=dict(color="white", width=1.5),
    ),
    text=[f"{v:,}" for v in psi_cnt["Total"]],
    textposition="outside",
    textfont=dict(size=11, color=S_DARK, family="monospace"),
    hovertemplate="<b>%{x}</b><br>Total: %{y:,}<extra></extra>",
))
apply_clean_layout(fig_psi, height=340, extra=dict(
    showlegend=False,
    xaxis=dict(title="Psicólogo", tickangle=-30, tickfont=dict(size=11)),
    yaxis=dict(title="N° citas"),
    bargap=0.3,
))
st.plotly_chart(fig_psi, use_container_width=True)
st.caption("💡 Un desbalance grande entre psicólogos puede indicar que algunos tienen poca visibilidad o disponibilidad registrada.")


# ── Tasa de asistencia por psicólogo ──────────────────────────────────────────
st.markdown("**🎯 Tasa de asistencia por psicólogo**")
psi_cnt["Completadas"] = psi_cnt["Realizadas"] + (
    df_citas.groupby("nombrePsicologo")["estado"]
    .apply(lambda s: (s=="No Asistió").sum())
    .reindex(psi_cnt["nombrePsicologo"])
    .values
)
psi_cnt["TasaAsist"] = np.where(
    psi_cnt["Completadas"] > 0,
    psi_cnt["Realizadas"] / psi_cnt["Completadas"] * 100,
    np.nan
)
lol_psi = psi_cnt.dropna(subset=["TasaAsist"]).sort_values("TasaAsist")

if len(lol_psi) > 0:
    fig_lol_psi = go.Figure()
    for i, row in lol_psi.iterrows():
        color = PINKS[i % len(PINKS)]
        fig_lol_psi.add_trace(go.Scatter(
            x=[0, row["TasaAsist"]], y=[row["nombrePsicologo"], row["nombrePsicologo"]],
            mode="lines", line=dict(color=color, width=2),
            showlegend=False, hoverinfo="skip",
        ))
        fig_lol_psi.add_trace(go.Scatter(
            x=[row["TasaAsist"]], y=[row["nombrePsicologo"]],
            mode="markers+text",
            marker=dict(size=16, color=color, line=dict(color="white", width=2)),
            text=[f"  {row['TasaAsist']:.1f}%"],
            textposition="middle right",
            textfont=dict(size=10, color=S_DARK),
            showlegend=False,
            hovertemplate=f"<b>{row['nombrePsicologo']}</b><br>Asistencia: {row['TasaAsist']:.1f}%<br>Realizadas: {int(row['Realizadas'])}<extra></extra>",
        ))
    apply_clean_layout(fig_lol_psi, height=max(280, len(lol_psi)*52), extra=dict(
        showlegend=False,
        xaxis=dict(title="Tasa de asistencia (%)", range=[0, 115]),
        yaxis=dict(tickfont=dict(size=11, color="#333333")),
    ))
    fig_lol_psi.add_vline(x=80, line=dict(color="#fb923c", width=1.5, dash="dash"))
    fig_lol_psi.add_annotation(
        x=80, y=0, text="80% ref.", showarrow=False,
        font=dict(size=9, color="#fb923c"), xanchor="left",
    )
    st.plotly_chart(fig_lol_psi, use_container_width=True)
    st.caption("💡 La línea naranja marca el 80% como referencia.")
else:
    st.info("No hay suficientes citas completadas para calcular la tasa de asistencia por psicólogo.")


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Evolución temporal
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Evolución temporal de citas</div>",
            unsafe_allow_html=True)

st.markdown("**📅 Volumen de citas agendadas por fecha**")
ts_df = df_citas.dropna(subset=["fechaCita"]).copy()

if len(ts_df) > 0:
    ts_agg = (
        ts_df.groupby("fechaCita")
        .size()
        .reset_index(name="N")
        .sort_values("fechaCita")
    )
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=ts_agg["fechaCita"], y=ts_agg["N"],
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(236, 72, 153, 0.07)",
        line=dict(color=S_MED, width=2.5, shape="spline"),
        marker=dict(size=7, color=S_DARK, line=dict(color="white", width=1.5)),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Citas: %{y:,}<extra></extra>",
    ))
    apply_clean_layout(fig_ts, height=300, extra=dict(
        xaxis=dict(title="Fecha", tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(title="N° citas agendadas", rangemode="tozero"),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
    ))
    st.plotly_chart(fig_ts, use_container_width=True)
    st.caption("💡 Picos altos pueden indicar periodos de alta demanda.")

    st.markdown("**📆 Distribución de citas por día de la semana**")
    ts_df["diaSemana"] = ts_df["fechaCita"].dt.dayofweek
    ts_df["diaNombre"] = ts_df["diaSemana"].map(DIAS_ES)
    dia_cnt = (
        ts_df.groupby(["diaSemana","diaNombre"])
        .size()
        .reset_index(name="N")
        .sort_values("diaSemana")
    )
    fig_dia = go.Figure(go.Bar(
        x=dia_cnt["diaNombre"],
        y=dia_cnt["N"],
        marker=dict(
            color=dia_cnt["N"],
            colorscale=[[0, S_PALE],[0.5, S_BASE],[1, S_DARK]],
            showscale=False,
            line=dict(color="white", width=1.5),
        ),
        text=[f"{v:,}" for v in dia_cnt["N"]],
        textposition="outside",
        textfont=dict(size=11, color=S_DARK, family="monospace"),
        hovertemplate="<b>%{x}</b><br>Citas: %{y:,}<extra></extra>",
    ))
    apply_clean_layout(fig_dia, height=320, extra=dict(
        showlegend=False,
        xaxis=dict(title="Día de la semana"),
        yaxis=dict(title="N° citas"),
        bargap=0.3,
    ))
    st.plotly_chart(fig_dia, use_container_width=True)
    st.caption("💡 Conocer los días de mayor demanda permite planificar mejor las disponibilidades.")
else:
    st.info("No hay datos de fecha en las citas registradas.")


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Top estudiantes
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Estudiantes con mayor actividad</div>",
            unsafe_allow_html=True)

st.markdown("**🎓 Top 10 estudiantes por número de citas agendadas**")
est_cnt = (
    df_citas.groupby("estudianteId")
    .agg(Total=("citaId","count"),
         Realizadas=("estado", lambda s: (s=="Realizada").sum()))
    .reset_index()
    .nlargest(10,"Total")
    .sort_values("Total")
)
if not df_est.empty:
    est_cnt = est_cnt.merge(
        df_est[["estudianteId","nombreCompleto"]], on="estudianteId", how="left"
    )
    est_cnt["label"] = est_cnt["nombreCompleto"].fillna(est_cnt["estudianteId"])
else:
    est_cnt["label"] = est_cnt["estudianteId"]

fig_est = go.Figure()
for i, row in est_cnt.iterrows():
    color = PINKS[i % len(PINKS)]
    fig_est.add_trace(go.Scatter(
        x=[0, row["Total"]], y=[row["label"], row["label"]],
        mode="lines", line=dict(color=color, width=2),
        showlegend=False, hoverinfo="skip",
    ))
    fig_est.add_trace(go.Scatter(
        x=[row["Total"]], y=[row["label"]],
        mode="markers+text",
        marker=dict(size=16, color=color, line=dict(color="white", width=2)),
        text=[f"  {int(row['Total']):,}"],
        textposition="middle right",
        textfont=dict(size=10, color=S_DARK),
        showlegend=False,
        hovertemplate=f"<b>{row['label']}</b><br>Citas: {int(row['Total']):,}<extra></extra>",
    ))
apply_clean_layout(fig_est, height=max(280, len(est_cnt)*52), extra=dict(
    showlegend=False,
    xaxis=dict(title="N° citas agendadas", range=[0, est_cnt["Total"].max()*1.2]),
    yaxis=dict(tickfont=dict(size=11, color="#333333")),
))
st.plotly_chart(fig_est, use_container_width=True)
st.caption("💡 Estudiantes con muchas citas pueden necesitar acompañamiento continuo.")


# ── TABLA RESUMEN ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Resumen por estado</div>",
            unsafe_allow_html=True)
st.markdown("**📋 Conteo y porcentaje por estado de cita**")
resumen = (
    df_citas.groupby("estado")
    .size()
    .reset_index(name="N")
    .sort_values("N", ascending=False)
)
resumen["Porcentaje"] = (resumen["N"] / resumen["N"].sum() * 100).round(1).astype(str) + "%"
resumen.columns = ["Estado","Citas","Porcentaje"]
resumen = resumen.set_index("Estado")
st.dataframe(resumen, use_container_width=True, height=220)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<hr style='border:1px solid {S_PALE}; margin:28px 0 10px 0;'>
<p style='text-align:center; color:#9d174d; font-size:0.75rem;'>
    SerenityLab &nbsp;|&nbsp; Backend: localhost:8080 &nbsp;|&nbsp;
    Streamlit · Plotly
</p>
""", unsafe_allow_html=True)