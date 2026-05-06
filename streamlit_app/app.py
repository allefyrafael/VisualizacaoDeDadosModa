import streamlit as st

from utils.theme import page_setup, hero, section_header, kpi_card, kpi_grid, footer
from utils.data_loader import load_data, kpis
from utils.i18n import t, language_selector

page_setup("Home", icon="👗")

language_selector()

df = load_data()
m = kpis(df)

hero(
    eyebrow=t("home.hero.eyebrow"),
    title_html=t("home.hero.title"),
    subtitle=t("home.hero.subtitle"),
)

kpi_grid([
    kpi_card(t("home.kpi.products"), f"{m['total']:,}".replace(",", "."), trend=t("home.kpi.products.trend")),
    kpi_card(t("home.kpi.brands"), f"{m['marcas']}", trend=t("home.kpi.brands.trend")),
    kpi_card(t("home.kpi.rating"), f"{m['nota_media']:.2f}", unit="/5", trend=t("home.kpi.rating.trend")),
    kpi_card(t("home.kpi.ticket"), f"R$ {m['preco_medio']:.0f}", trend=t("home.kpi.ticket.trend.tpl", f"{m['preco_mediano']:.0f}")),
])

# Manifesto
st.markdown(
    f"""
    <div class="manifesto">
        <div class="manifesto-eyebrow">{t("home.manifesto.eyebrow")}</div>
        <p class="manifesto-lead">{t("home.manifesto.lead")}</p>
        <p class="manifesto-body">{t("home.manifesto.body")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

section_header(
    eyebrow=t("home.acts.eyebrow"),
    title=t("home.acts.title"),
    subtitle=t("home.acts.subtitle"),
)

# Cards uniformes — texto + CTA com arrow alinhado embaixo
def _nav_card(href: str, eyebrow: str, title: str, body: str, cta: str, variant: str = "") -> str:
    cls = f"nav-card-html {variant}".strip()
    return (
        f'<a href="{href}" target="_self" class="{cls}">'
        f'<div class="nav-card-eyebrow">{eyebrow}</div>'
        f'<div class="nav-card-title">{title}</div>'
        f'<div class="nav-card-body">{body}</div>'
        f'<div class="nav-card-cta"><span class="cta-text">{cta}</span><span class="cta-arrow">→</span></div>'
        f'</a>'
    )

st.markdown(
    "<div class='nav-grid-html'>"
    + _nav_card(
        "/Visao_Geral",
        t("home.card.dashboard.eyebrow"),
        t("home.card.dashboard.title"),
        t("home.card.dashboard.body"),
        t("home.card.dashboard.cta"),
    )
    + _nav_card(
        "/Analise_Exploratoria",
        t("home.card.analysis.eyebrow"),
        t("home.card.analysis.title"),
        t("home.card.analysis.body"),
        t("home.card.analysis.cta"),
    )
    + _nav_card(
        "/Insights_ML",
        t("home.card.ml.eyebrow"),
        t("home.card.ml.title"),
        t("home.card.ml.body"),
        t("home.card.ml.cta"),
        variant="is-ml",
    )
    + "</div>",
    unsafe_allow_html=True,
)

section_header(
    eyebrow=t("home.dataset.eyebrow"),
    title=t("home.dataset.title"),
    subtitle=t("home.dataset.subtitle"),
)

avaliacoes_fmt = f"{m['avaliacoes_total']:,}".replace(",", ".")

st.markdown(
    (
        '<div class="dataset-panel">'
        '<div class="dataset-stat">'
        '<div class="dataset-stat-icon" style="background:rgba(194,65,12,0.12); color:var(--primary);">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
        '</div>'
        f'<div class="dataset-stat-value">{avaliacoes_fmt}</div>'
        f'<div class="dataset-stat-label">{t("ml.kpi.reviews")}</div>'
        '</div>'
        '<div class="dataset-stat">'
        '<div class="dataset-stat-icon" style="background:rgba(212,165,116,0.18); color:#A16207;">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
        '</div>'
        f'<div class="dataset-stat-value">R$ {m["preco_medio"]:.2f}</div>'
        f'<div class="dataset-stat-label">{t("home.kpi.ticket")}</div>'
        '</div>'
        '<div class="dataset-stat">'
        '<div class="dataset-stat-icon" style="background:rgba(124,58,237,0.12); color:var(--plum);">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
        '</div>'
        f'<div class="dataset-stat-value">{m["nota_media"]:.2f}/5</div>'
        f'<div class="dataset-stat-label">{t("home.kpi.rating")}</div>'
        '</div>'
        '<div class="dataset-stat">'
        '<div class="dataset-stat-icon" style="background:rgba(8,145,178,0.12); color:var(--petrol);">'
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
        '</div>'
        f'<div class="dataset-stat-value">{m["marcas"]}</div>'
        f'<div class="dataset-stat-label">{t("home.kpi.brands")}</div>'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True,
)

footer()
