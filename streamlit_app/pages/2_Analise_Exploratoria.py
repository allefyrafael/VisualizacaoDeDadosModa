import streamlit as st

from utils.theme import page_setup, hero, section_header, footer, insight_box, chart_title, PLOTLY_CHART_CONFIG
from utils.data_loader import load_data
from utils.charts import (
    scatter_preco_avaliacoes,
    heatmap_corr,
    bar_top_marcas,
    pie_genero,
    density_preco_temporada,
)
from utils.i18n import t, language_selector

page_setup(t("nav.analysis"), icon="📈")

language_selector()

df = load_data()

hero(
    eyebrow=t("analysis.hero.eyebrow"),
    title_html=t("analysis.hero.title"),
    subtitle=t("analysis.hero.subtitle"),
)

st.markdown(
    (
        '<div class="story-flow">'
        '<div class="story-flow-eyebrow">METODOLOGIA · STORYTELLING WITH DATA</div>'
        '<div class="story-flow-grid">'
        f'<div class="story-cell"><div class="story-num">01</div><div class="story-name">{t("analysis.story.01")}</div></div>'
        '<div class="story-link"></div>'
        f'<div class="story-cell"><div class="story-num">02</div><div class="story-name">{t("analysis.story.02")}</div></div>'
        '<div class="story-link"></div>'
        f'<div class="story-cell"><div class="story-num">03</div><div class="story-name">{t("analysis.story.03")}</div></div>'
        '<div class="story-link"></div>'
        f'<div class="story-cell is-final"><div class="story-num">04</div><div class="story-name">{t("analysis.story.04")}</div></div>'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True,
)

tabs = st.tabs([
    t("analysis.tab.scatter"),
    t("analysis.tab.heatmap"),
    t("analysis.tab.bars"),
    t("analysis.tab.pie"),
    t("analysis.tab.density"),
])

with tabs[0]:
    section_header(t("analysis.q1.eyebrow"), t("analysis.q1.title"), t("analysis.q1.sub"))
    chart_title(t("analysis.q1.chart.title"), t("analysis.q1.chart.sub"))
    st.plotly_chart(scatter_preco_avaliacoes(df), use_container_width=True, config=PLOTLY_CHART_CONFIG)

    pop = df.dropna(subset=["N_Avaliações", "Preço"])
    top_pop = pop.nlargest(50, "N_Avaliações")
    insight_box(
        f"<strong>R$ {top_pop['Preço'].mean():.2f}</strong> · "
        f"{(top_pop['Preço'].mean() / df['Preço'].mean() - 1) * 100:+.1f}%",
        label=t("analysis.read"),
    )

with tabs[1]:
    section_header(t("analysis.q2.eyebrow"), t("analysis.q2.title"), t("analysis.q2.sub"))
    chart_title(t("analysis.q2.chart.title"), t("analysis.q2.chart.sub"))
    st.plotly_chart(heatmap_corr(df), use_container_width=True, config=PLOTLY_CHART_CONFIG)

    corr_qa = df[["N_Avaliações", "Qtd_Vendidos_Num"]].corr().iloc[0, 1]
    corr_pn = df[["Preço", "Nota"]].corr().iloc[0, 1]
    insight_box(
        f"avaliações × vendidos = <strong>{corr_qa:.2f}</strong> · "
        f"preço × nota = <strong>{corr_pn:.2f}</strong>",
        label=t("analysis.read"),
    )

with tabs[2]:
    section_header(t("analysis.q3.eyebrow"), t("analysis.q3.title"), t("analysis.q3.sub"))
    chart_title(t("analysis.q3.chart.title"), t("analysis.q3.chart.sub"))
    st.plotly_chart(bar_top_marcas(df, n=10), use_container_width=True, config=PLOTLY_CHART_CONFIG)

    top1 = df["Marca"].value_counts().head(1)
    insight_box(
        f"<strong>{top1.index[0]}</strong> · {int(top1.iloc[0])} ({top1.iloc[0]/len(df)*100:.1f}%)",
        label=t("analysis.read"),
    )

with tabs[3]:
    section_header(t("analysis.q4.eyebrow"), t("analysis.q4.title"), t("analysis.q4.sub"))
    chart_title(t("analysis.q4.chart.title"), t("analysis.q4.chart.sub"))
    st.plotly_chart(pie_genero(df), use_container_width=True, config=PLOTLY_CHART_CONFIG)

    g = df["Gênero"].value_counts(normalize=True) * 100
    top_genero = g.head(1)
    insight_box(
        f"<strong>{top_genero.index[0]}</strong> · <strong>{top_genero.iloc[0]:.1f}%</strong>",
        label=t("analysis.read"),
    )

with tabs[4]:
    section_header(t("analysis.q5.eyebrow"), t("analysis.q5.title"), t("analysis.q5.sub"))
    chart_title(t("analysis.q5.chart.title"), t("analysis.q5.chart.sub"))
    st.plotly_chart(density_preco_temporada(df), use_container_width=True, config=PLOTLY_CHART_CONFIG)

    medians = df.groupby("Temporada")["Preço"].median().sort_values(ascending=False)
    insight_box(
        f"<strong>{medians.index[0]}</strong> R$ {medians.iloc[0]:.2f} · "
        f"<strong>{medians.index[-1]}</strong> R$ {medians.iloc[-1]:.2f}",
        label=t("analysis.read"),
    )

footer()
