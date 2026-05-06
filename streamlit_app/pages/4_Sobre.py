import streamlit as st

from utils.theme import page_setup, hero, section_header, footer
from utils.i18n import t, language_selector

AUTHOR_URL = "https://allefyrafael.codes"
SOCIAL = {
    "github": "https://github.com/allefyrafael",
    "linkedin": "https://www.linkedin.com/in/allefyrafael",
}

page_setup(t("nav.about"), icon="ℹ️")

language_selector()

hero(
    eyebrow=t("about.hero.eyebrow"),
    title_html=t("about.hero.title"),
    subtitle=t("about.hero.subtitle"),
)

c1, c2 = st.columns([1.2, 1])

with c1:
    section_header(t("about.motivation.eyebrow"), t("about.motivation.title"))
    st.markdown(t("about.motivation.body"))

with c2:
    st.markdown(
        f"""
        <div style="background:var(--bg-white); border:1px solid var(--line); border-radius:20px; padding:28px;">
            <div style="font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--gold); margin-bottom:16px;">{t("about.stack.eyebrow")}</div>
            <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:12px;">
                <li><strong>Streamlit</strong></li>
                <li><strong>Plotly</strong></li>
                <li><strong>Pandas + NumPy</strong></li>
                <li><strong>Scikit-learn</strong></li>
                <li><strong>HTML + CSS custom</strong></li>
                <li><strong>Streamlit Community Cloud</strong></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

section_header(t("about.arch.eyebrow"), t("about.arch.title"), t("about.arch.subtitle"))

st.code(
    """
streamlit_app/
├── app.py                          # Home / landing
├── pages/
│   ├── 1_Visao_Geral.py            # Dashboard
│   ├── 2_Analise_Exploratoria.py   # 5 charts
│   ├── 3_Insights_ML.py            # ML + NLP
│   └── 4_Sobre.py
├── utils/
│   ├── data_loader.py
│   ├── charts.py
│   ├── theme.py
│   └── i18n.py                     # PT/EN/ES
├── assets/style.css
├── .streamlit/config.toml
└── requirements.txt
    """,
    language="text",
)

section_header(t("about.author.eyebrow"), t("about.author.title"), t("about.author.subtitle"))

st.markdown(
    f"""
    <div class="author-card">
        <h2>
            <a class="author-name-link" href="{AUTHOR_URL}" target="_blank" rel="noopener noreferrer">Allefy Rafael</a>
        </h2>
        <p class="author-tagline">{t("about.author.subtitle")}</p>
        <div class="author-actions">
            <a class="btn-portfolio" href="{AUTHOR_URL}" target="_blank" rel="noopener noreferrer">{t("about.btn.portfolio")} →</a>
            <a class="btn-ghost" href="{SOCIAL['github']}" target="_blank" rel="noopener noreferrer">GitHub →</a>
            <a class="btn-ghost" href="{SOCIAL['linkedin']}" target="_blank" rel="noopener noreferrer">LinkedIn →</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

footer()
