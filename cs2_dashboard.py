import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="CS2 Skin Tracker",
    page_icon="🎯",
    layout="wide",
)

# ── CSS customizado (dark gaming) ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

html, body {
    font-family: 'Rajdhani', sans-serif;
    background-color: #060d14;
    color: #e2e8f0;
}
.stApp { background-color: #060d14; }
.stApp * { font-family: 'Rajdhani', sans-serif; }

/* Header */
.cs2-header {
    background: linear-gradient(135deg, #0a1628 0%, #060d14 100%);
    border-bottom: 1px solid #1a2f45;
    padding: 18px 28px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 28px;
    border-radius: 12px;
}
.cs2-header h1 {
    font-size: 24px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;
}
.cs2-header p {
    font-size: 11px;
    color: #4a7a9b;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #0d1f2e 0%, #0a1826 100%);
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    margin-bottom: 4px;
    height: 100%;
}
.kpi-accent {
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 12px 0 0 12px;
}
.kpi-label {
    font-size: 10px;
    color: #4a7a9b;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}
.kpi-sub {
    font-size: 11px;
    color: #4a7a9b;
    margin-top: 5px;
}

/* Chart card */
.chart-card {
    background: #0d1f2e;
    border: 1px solid #1a2f45;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}
.chart-title {
    font-size: 11px;
    font-weight: 700;
    color: #f97316;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a1628 !important;
    border-right: 1px solid #1a2f45 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #94a3b8 !important;
}

/* Botão fechar (dentro da sidebar) */
[data-testid="stSidebarCollapseButton"] button,
/* Botão abrir (fora da sidebar) */
[data-testid="stExpandSidebarButton"] {
    background-color: #0a1628 !important;
    border: none !important;
}

[data-testid="stSidebarCollapseButton"] button span,
[data-testid="stExpandSidebarButton"] span {
    color: #f97316 !important;
    font-family: 'Material Symbols Rounded' !important;
}

/* Tabs */
[data-testid="stTab"] {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Remove streamlit branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────────────────────
RAW = [
    ("Survival marble fade FN", 1215, 1500),
    ("Survival rust coat BS 0.51", 490, 600),
    ("Ak inheritance FT 0.28", 315, 385),
    ("Sticker Fallen gold", 42, 94),
    ("Sticker Fallen gold", 42, 94),
    ("Sticker Fallen gold", 43, 96),
    ("Sticker Fallen holo", 24, 50),
    ("Sticker Fallen holo", 24, 50),
    ("Sticker Fallen holo", 24, 50),
    ("Sticker Fallen holo", 25, 52),
    ("Survival rust coat BS 0.69", 470, 650),
    ("Survival rust coat BS 0.61", 470, 580),
    ("Survival marble fade FN 0.01", 1220, 1450),
    ("Sticker Fallen holo", 35, 90),
    ("Survival rust coat 0.60", 485, 550),
    ("Nomad rust coat 0.65", 980, 1080),
    ("M4a1 vaporwave ft", 350, 418),
    ("M4a4 polysoup ft", 35, 60),
    ("Awp Redline ft st 0.22", 685, 800),
    ("Souvenir Charm Strikes back", 200, 270),
    ("Ak inheritance FT 0.18", 350, 400),
    ("Mac neon rider ft", 50, 320),
    ("Mp9 starlight protector mw", 50, 300),
    ("Famas bad trip mw", 40, 300),
    ("Ssg dragonfire mw", 150, 300),
    ("M4a1 cyrex", 250, 600),
    ("Mac neon rider mw", 60, 320),
    ("Bizon anubis fn", 130, 500),
    ("Bizon anubis fn", 130, 500),
    ("Ssg dragonfire ft", 610, 1480),
    ("Famas mecha ft 6x", 470, 900),
    ("Awp man o war mw", 350, 450),
    ("Awp redline ft st 0.23", 800, 950),
    ("Ak the empress mw", 350, 450),
    ("P250 see ya later", 250, 430),
    ("Eagle conspiracy", 52, 98),
    ("P90 trigon", 85, 100),
    ("M4a1 leaded glass 3x", 96, 130),
    ("P250 muertos", 44, 67),
    ("Berettas melondrama 2x", 54, 76),
    ("M4a1 cyrex", 600, 800),
    ("Eagle printstream", 240, 300),
    ("Galil eco ft", 41, 73),
    ("Bayonet doppler phase 2", 2800, 3400),
    ("Awp cmyk ft 0.15", 1170, 1800),
    ("Falchion lore ft", 670, 800),
    ("M4a1 vaporwave mw", 840, 950),
    ("M9 lore ft", 2600, 2815),
    ("M4a1 vaporwave mw", 800, 900),
    ("Ak nightwish ft", 250, 350),
    ("Fallen gold 2025 austin", 42, 90),
    ("Awp black nile ft", 17, 50),
    ("Fallen holo shanghai x3", 100, 200),
    ("M4a1 vaporwave ft", 750, 845),
    ("P250 apeps curse", 350, 525),
    ("Awp black nile fn x3", 133, 180),
    ("Famas waters nephtys", 190, 262),
    ("Falchion lore ft", 550, 700),
    ("Gloves Crimson web ft", 800, 950),
    ("Bayonet Marble fade", 1800, 2030),
    ("Falchion lore mw", 650, 720),
    ("Glock axia fn", 400, 1250),
    ("Ak inheritance ft", 315, 400),
    ("Classic Crimson web", 800, 910),
    ("Eagle heat treated", 120, 370),
    ("Bayonet Doppler Phase 2", 2550, 2750),
    ("Mp7 fade", 100, 200),
    ("Eagle heat treated", 400, 630),
    ("M4a4 temukau", 210, 250),
    ("Gloves mogul ft", 670, 723),
    ("Eagle cobalt disruption", 820, 1250),
    ("Usp printstream mw", 330, 390),
    ("Butterfly freehand", 3300, 3625),
]

TAXA = 0.06

CAT_COLORS = {
    "Rifle/AWP": "#f97316",
    "Faca":      "#a855f7",
    "Pistola":   "#3b82f6",
    "SMG":       "#10b981",
    "Luvas":     "#ec4899",
    "Sticker":   "#eab308",
    "Outros":    "#6b7280",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0a1520",
    font=dict(family="Rajdhani, sans-serif", color="#94a3b8"),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor="#1a2f45", zerolinecolor="#1a2f45"),
    yaxis=dict(gridcolor="#1a2f45", zerolinecolor="#1a2f45"),
)

def categorize(nome: str) -> str:
    n = nome.lower()
    if any(x in n for x in ["sticker", "fallen gold", "fallen holo", "fallen gold 2025", "fallen holo shanghai"]):
        return "Sticker"
    if any(x in n for x in ["bayonet", "falchion", "m9", "butterfly", "karambit"]):
        return "Faca"
    if any(x in n for x in ["gloves", "classic crimson"]):
        return "Luvas"
    if any(x in n for x in ["ak", "m4a1", "m4a4", "awp", "famas", "galil", "ssg", "survival", "nomad"]):
        return "Rifle/AWP"
    if any(x in n for x in ["glock", "p250", "usp", "eagle", "berettas", "desert"]):
        return "Pistola"
    if any(x in n for x in ["mac", "mp9", "bizon", "mp7", "p90"]):
        return "SMG"
    return "Outros"

@st.cache_data
def load_data():
    rows = []
    for nome, compra, venda in RAW:
        taxa     = venda * TAXA
        rec_liq  = venda - taxa
        lucro    = rec_liq - compra
        roi      = round((lucro / compra) * 100, 2)
        rows.append(dict(
            nome=nome, compra=compra, venda_bruto=venda,
            taxa=taxa, receita_liq=rec_liq,
            lucro=round(lucro, 2), roi=roi,
            categoria=categorize(nome),
        ))
    return pd.DataFrame(rows)

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cs2-header">
  <span style="font-size:32px">🎯</span>
  <div>
    <h1>CS2 Skin Tracker</h1>
    <p>Trading Analytics Dashboard</p>
  </div>
  <div style="margin-left:auto;text-align:right">
    <div style="font-size:10px;color:#4a7a9b;letter-spacing:2px;text-transform:uppercase">Total de Trades</div>
    <div style="font-size:28px;font-weight:700;color:#f97316;font-family:'JetBrains Mono'">{}</div>
  </div>
</div>
""".format(len(df)), unsafe_allow_html=True)

# ── Sidebar — Filtros ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 Filtros")
    cats = st.multiselect(
        "Categoria",
        options=sorted(df["categoria"].unique()),
        default=sorted(df["categoria"].unique()),
    )
    roi_min, roi_max = float(df["roi"].min()), float(df["roi"].max())
    roi_range = st.slider("ROI (%)", roi_min, roi_max, (roi_min, roi_max), step=1.0)
    st.markdown("---")
    st.markdown(f"**Trades filtrados:** {len(df[(df['categoria'].isin(cats)) & (df['roi'].between(*roi_range))])}")

dff = df[df["categoria"].isin(cats) & df["roi"].between(*roi_range)].copy()

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_inv   = dff["compra"].sum()
total_venda = dff["venda_bruto"].sum()
total_lucro = dff["lucro"].sum()
roi_geral   = (total_lucro / total_inv * 100) if total_inv else 0
melhor_roi  = dff.loc[dff["roi"].idxmax()] if len(dff) else None
sucesso_pct = (dff["lucro"] > 0).mean() * 100 if len(dff) else 0

KPIS = [
    ("💼 Total Investido",   f"R$ {total_inv:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "capital alocado",          "#3b82f6"),
    ("💵 Receita Total",     f"R$ {total_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "vendas brutas",           "#8b5cf6"),
    ("✅ Lucro Líquido",     f"R$ {total_lucro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "após taxa 6%",            "#10b981"),
    ("📈 ROI Geral",         f"{roi_geral:.1f}%",                                                             "retorno médio", "#f97316"),
    ("🔥 Melhor ROI",        f"{melhor_roi['roi']:.1f}%" if melhor_roi is not None else "—",                  melhor_roi["nome"][:20] + "…" if melhor_roi is not None else "", "#ec4899"),
    ("🏆 Taxa de Sucesso",   f"{sucesso_pct:.0f}%",                                                           f"{(dff['lucro']>0).sum()}/{len(dff)} trades lucrativos",         "#eab308"),
]

cols = st.columns(6)
for col, (label, val, sub, color) in zip(cols, KPIS):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-accent" style="background:{color}"></div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Visão Geral", "🗂️  Por Categoria", "📋  Todos os Trades"])

# ── TAB 1 — Visão Geral ───────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns(2)

    # Top 10 ROI
    with col1:
        st.markdown('<div class="chart-title">🔥 TOP 10 — MAIOR ROI (%)</div>', unsafe_allow_html=True)
        top_roi = dff.nlargest(11, "roi")[["nome", "roi", "lucro", "categoria"]].copy()
        top_roi["nome_curto"] = top_roi["nome"].str[:24]
        fig = go.Figure(go.Bar(
            x=top_roi["roi"],
            y=top_roi["nome_curto"],
            orientation="h",
            marker=dict(
                color=[CAT_COLORS.get(c, "#6b7280") for c in top_roi["categoria"]],
                opacity=0.9,
            ),
            customdata=top_roi[["lucro", "categoria"]].values,
            hovertemplate="<b>%{y}</b><br>ROI: %{x:.1f}%<br>Lucro: R$ %{customdata[0]:.2f}<br>Cat: %{customdata[1]}<extra></extra>",
        ))
        fig.update_layout(**PLOTLY_THEME, height=300)
        fig.update_xaxes(ticksuffix="%")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Top 10 Lucro
    with col2:
        st.markdown('<div class="chart-title">💰 TOP 10 — MAIOR LUCRO (R$)</div>', unsafe_allow_html=True)
        top_lucro = dff.nlargest(11, "lucro")[["nome", "roi", "lucro", "categoria"]].copy()
        top_lucro["nome_curto"] = top_lucro["nome"].str[:24]
        fig2 = go.Figure(go.Bar(
            x=top_lucro["lucro"],
            y=top_lucro["nome_curto"],
            orientation="h",
            marker=dict(
                color=[CAT_COLORS.get(c, "#6b7280") for c in top_lucro["categoria"]],
                opacity=0.9,
            ),
            customdata=top_lucro[["roi", "categoria"]].values,
            hovertemplate="<b>%{y}</b><br>Lucro: R$ %{x:.2f}<br>ROI: %{customdata[0]:.1f}%<br>Cat: %{customdata[1]}<extra></extra>",
        ))
        fig2.update_layout(**PLOTLY_THEME, height=300)
        fig2.update_xaxes(tickprefix="R$ ")
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter: Investimento vs Lucro
    st.markdown('<div class="chart-title">📈 INVESTIMENTO × LUCRO — todos os trades</div>', unsafe_allow_html=True)
    fig3 = px.scatter(
        dff, x="compra", y="lucro", color="categoria",
        color_discrete_map=CAT_COLORS,
        hover_name="nome",
        hover_data={"compra": ":,.2f", "lucro": ":,.2f", "roi": ":.1f"},
        labels={"compra": "Compra (R$)", "lucro": "Lucro (R$)", "roi": "ROI (%)"},
        size_max=12,
    )
    fig3.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=1, color="#060d14")))
    fig3.update_layout(**PLOTLY_THEME, height=340, legend=dict(
        bgcolor="rgba(0,0,0,0)", bordercolor="#1a2f45", borderwidth=1,
        font=dict(color="#94a3b8", size=11),
    ))
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 2 — Por Categoria ─────────────────────────────────────────────────────
with tab2:
    cat_df = dff.groupby("categoria").agg(
        lucro_total=("lucro", "sum"),
        trades=("lucro", "count"),
        roi_medio=("roi", "mean"),
        compra_total=("compra", "sum"),
    ).reset_index().sort_values("lucro_total", ascending=False)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="chart-title">🗂️ LUCRO TOTAL POR CATEGORIA</div>', unsafe_allow_html=True)
        fig4 = go.Figure(go.Pie(
            labels=cat_df["categoria"],
            values=cat_df["lucro_total"],
            hole=0.55,
            marker=dict(colors=[CAT_COLORS.get(c, "#6b7280") for c in cat_df["categoria"]]),
            hovertemplate="<b>%{label}</b><br>Lucro: R$ %{value:.2f}<br>%{percent}<extra></extra>",
        ))
        fig4.update_layout(**PLOTLY_THEME, height=320, showlegend=True,
                           legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")))
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.markdown('<div class="chart-title">📊 ROI MÉDIO POR CATEGORIA</div>', unsafe_allow_html=True)
        fig5 = go.Figure(go.Bar(
            x=cat_df["categoria"],
            y=cat_df["roi_medio"],
            marker=dict(color=[CAT_COLORS.get(c, "#6b7280") for c in cat_df["categoria"]], opacity=0.9),
            hovertemplate="<b>%{x}</b><br>ROI Médio: %{y:.1f}%<extra></extra>",
        ))
        fig5.update_layout(**PLOTLY_THEME, height=320)
        fig5.update_yaxes(ticksuffix="%")
        fig5.update_traces(marker_line_width=0)
        st.plotly_chart(fig5, use_container_width=True)

    # Tabela de categorias
    st.markdown('<div class="chart-title">📋 RESUMO POR CATEGORIA</div>', unsafe_allow_html=True)
    cat_display = cat_df.copy()
    cat_display.columns = ["Categoria", "Lucro Total", "Trades", "ROI Médio (%)", "Investimento Total"]
    cat_display["Lucro Total"] = cat_display["Lucro Total"].map("R$ {:,.2f}".format)
    cat_display["Investimento Total"] = cat_display["Investimento Total"].map("R$ {:,.2f}".format)
    cat_display["ROI Médio (%)"] = cat_display["ROI Médio (%)"].map("{:.1f}%".format)
    st.dataframe(cat_display, use_container_width=True, hide_index=True)

# ── TAB 3 — Tabela completa ───────────────────────────────────────────────────
with tab3:
    sort_col = st.selectbox("Ordenar por:", ["roi", "lucro", "compra", "venda_bruto"], format_func=lambda x: {
        "roi": "ROI (%)", "lucro": "Lucro (R$)", "compra": "Compra (R$)", "venda_bruto": "Venda (R$)"
    }.get(x, x))

    table = dff.sort_values(sort_col, ascending=False).reset_index(drop=True)
    table.index += 1

    display = table[["nome", "categoria", "compra", "venda_bruto", "taxa", "receita_liq", "lucro", "roi"]].copy()
    display.columns = ["Skin", "Categoria", "Compra (R$)", "Venda (R$)", "Taxa (R$)", "Receita Líq. (R$)", "Lucro (R$)", "ROI (%)"]

    st.dataframe(
        display.style
            .format({
                "Compra (R$)": "R$ {:.2f}",
                "Venda (R$)": "R$ {:.2f}",
                "Taxa (R$)": "R$ {:.2f}",
                "Receita Líq. (R$)": "R$ {:.2f}",
                "Lucro (R$)": "R$ {:.2f}",
                "ROI (%)": "{:.1f}%",
            })
            .applymap(lambda v: "color: #10b981; font-weight:bold" if isinstance(v, float) and v > 0 else
                                "color: #ef4444; font-weight:bold" if isinstance(v, float) and v < 0 else "",
                      subset=["Lucro (R$)"])
            .applymap(lambda v: "color: #10b981" if isinstance(v, str) and v.endswith("%") and float(v[:-1]) >= 50 else
                                "color: #f97316" if isinstance(v, str) and v.endswith("%") and float(v[:-1]) >= 20 else
                                "color: #eab308" if isinstance(v, str) and v.endswith("%") else "",
                      subset=["ROI (%)"]),
        use_container_width=True,
        height=520,
    )

    st.markdown(f"""
    <div style="display:flex;gap:32px;margin-top:16px;font-size:12px;color:#4a7a9b;letter-spacing:1px">
      <span>TRADES: <strong style="color:#fff">{len(table)}</strong></span>
      <span>INVESTIDO: <strong style="color:#3b82f6">R$ {table['compra'].sum():,.2f}</strong></span>
      <span>LUCRO: <strong style="color:#10b981">R$ {table['lucro'].sum():,.2f}</strong></span>
      <span>ROI MÉDIO: <strong style="color:#f97316">{table['roi'].mean():.1f}%</strong></span>
    </div>
    """, unsafe_allow_html=True)