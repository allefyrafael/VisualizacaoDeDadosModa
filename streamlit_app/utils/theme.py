from pathlib import Path
import streamlit as st

COLORS = {
    "bg": "#FAF7F2",
    "bg_white": "#FFFFFF",
    "primary": "#C2410C",
    "primary_soft": "#F4E4DC",
    "ink": "#1F2937",
    "ink_soft": "#4B5563",
    "muted": "#9CA3AF",
    "gold": "#D4A574",
    "line": "#E7E2D9",
    "plum": "#7C3AED",
    "moss": "#059669",
    "petrol": "#0891B2",
}

PALETTE = [
    COLORS["primary"],
    COLORS["gold"],
    COLORS["plum"],
    COLORS["moss"],
    COLORS["petrol"],
    "#DC2626",
    "#0EA5E9",
    "#A16207",
]

PLOTLY_LAYOUT = dict(
    font=dict(family="DM Sans, sans-serif", color=COLORS["ink"], size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title_font=dict(family="Playfair Display, serif", size=20, color=COLORS["ink"]),
    margin=dict(l=20, r=24, t=76, b=44),
    xaxis=dict(gridcolor=COLORS["line"], zerolinecolor=COLORS["line"]),
    yaxis=dict(gridcolor=COLORS["line"], zerolinecolor=COLORS["line"]),
    legend=dict(font=dict(size=12)),
)

# Passed to st.plotly_chart(..., config=...)
PLOTLY_CHART_CONFIG: dict[str, bool] = {
    "displaylogo": False,
}

_CSS_PATH = Path(__file__).parent.parent / "assets" / "style.css"

# CSS crítico inline para evitar FOUC (flash of unstyled content).
# Aplicado antes de qualquer markdown subsequente — pinta a sidebar e o menu
# de itens com o look final no PRIMEIRO frame, sem esperar o style.css externo.
_CRITICAL_CSS = """
:root {
    --bg-cream: #FAF7F2;
    --bg-white: #FFFFFF;
    --primary: #C2410C;
    --primary-soft: #F4E4DC;
    --ink: #1F2937;
    --ink-soft: #4B5563;
    --muted: #9CA3AF;
    --gold: #D4A574;
    --line: #E7E2D9;
    --plum: #7C3AED;
}
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #FAF7F2 !important;
    color: #1F2937;
    font-family: 'DM Sans', system-ui, -apple-system, sans-serif !important;
}
/* SIDEBAR base — pintada antes do React expor stSidebarNav */
[data-testid="stSidebar"],
section[data-testid="stSidebar"] {
    background: #F2EDE4 !important;
    border-right: 1px solid #E7E2D9 !important;
}
[data-testid="stSidebarNav"] {
    padding: 24px 16px !important;
}
[data-testid="stSidebarNav"]::before {
    content: 'NAVEGAÇÃO';
    display: block;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #D4A574;
    margin: 0 8px 12px;
    font-family: 'DM Sans', sans-serif;
}
/* MENU DE ITENS — links da multipage nav */
[data-testid="stSidebar"] ul {
    gap: 4px !important;
    padding-left: 0 !important;
    list-style: none !important;
}
[data-testid="stSidebar"] li {
    list-style: none !important;
}
[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a {
    padding: 12px 16px !important;
    border-radius: 10px !important;
    margin: 2px 0 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1F2937 !important;
    border: 1px solid transparent !important;
    text-decoration: none !important;
    transition: background 0.15s ease, color 0.15s ease, padding-left 0.15s ease;
    display: flex !important;
    align-items: center !important;
}
[data-testid="stSidebar"] a:hover {
    background: #F4E4DC !important;
    color: #C2410C !important;
    padding-left: 20px !important;
}
[data-testid="stSidebar"] a[aria-current="page"],
[data-testid="stSidebar"] li:has(> a[aria-current="page"]) > a {
    background: #C2410C !important;
    color: #FFFFFF !important;
    border-color: #C2410C !important;
    box-shadow: 0 4px 12px rgba(194, 65, 12, 0.25);
}
/* Mobile: esconde sidebar — também já pintado aqui pra não piscar */
@media (max-width: 900px) {
    [data-testid="stSidebar"] { display: none !important; width: 0 !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stMain"] { margin-left: 0 !important; width: 100% !important; }
}
/* Esconde watermark Streamlit imediatamente */
#MainMenu, [data-testid="stCommonFooter"] footer, footer[data-testid="stFooter"] {
    visibility: hidden !important;
    height: 0 !important;
}
"""


def inject_css() -> None:
    # 1. CSS crítico inline (evita flicker)
    st.markdown(f"<style>{_CRITICAL_CSS}</style>", unsafe_allow_html=True)
    # 2. CSS completo do projeto
    css = _CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_setup(title: str, icon: str = "👗") -> None:
    st.set_page_config(
        page_title=f"{title} — Moda em Dados",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()


def hero(eyebrow: str, title_html: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-eyebrow">{eyebrow}</div>
            <h1 class="hero-title">{title_html}</h1>
            <p class="hero-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(eyebrow: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="section-eyebrow">{eyebrow}</div>
        <h2 class="section-title">{title}</h2>
        <p class="section-sub">{subtitle}</p>
        """,
        unsafe_allow_html=True,
    )


def chart_title(title: str, subtitle: str = "") -> None:
    sub_html = f"<p class='chart-sub'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"<div class='chart-head'><h3 class='chart-title'>{title}</h3>{sub_html}</div>",
        unsafe_allow_html=True,
    )


def insight_box(text: str, label: str = "Insight") -> None:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">{label}</div>
            <p class="insight-text">{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, unit: str = "", trend: str = "") -> str:
    unit_html = f"<span class='unit'>{unit}</span>" if unit else ""
    trend_html = f"<div class='kpi-trend'>{trend}</div>" if trend else ""
    return (
        f"<div class='kpi-card'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}{unit_html}</div>"
        f"{trend_html}"
        f"</div>"
    )


def kpi_grid(cards: list[str]) -> None:
    st.markdown(
        f"<div class='kpi-grid'>{''.join(cards)}</div>",
        unsafe_allow_html=True,
    )


def footer() -> None:
    try:
        from utils.i18n import t
        body = t("footer.body")
    except Exception:
        body = (
            '<strong>Moda em Dados</strong> — Projeto de portfólio por '
            '<a href="https://allefyrafael.codes/" target="_blank" rel="noopener" class="footer-author">Allefy Rafael</a>'
        )
    st.markdown(f'<div class="footer">{body}</div>', unsafe_allow_html=True)
