import streamlit as st

from utils.theme import page_setup, hero, section_header, kpi_card, kpi_grid, footer, insight_box, chart_title, PLOTLY_CHART_CONFIG
from utils.data_loader import load_data, kpis
from utils.charts import bar_top_marcas, hist_notas
from utils.i18n import t, language_selector

page_setup(t("nav.overview"), icon="📊")

language_selector()

df = load_data()

hero(
    eyebrow=t("overview.hero.eyebrow"),
    title_html=t("overview.hero.title"),
    subtitle=t("overview.hero.subtitle"),
)

generos_opts = sorted(df["Gênero"].unique().tolist())
temporadas_opts = sorted(df["Temporada"].unique().tolist())
marcas_opts = sorted(df["Marca"].unique().tolist())
preco_min, preco_max = float(df["Preço"].min()), float(df["Preço"].max())

f1, f2, f3, f4, f5, f6 = st.columns([1.2, 1.2, 1.2, 1.4, 1.4, 0.8])

with f1:
    with st.popover(t("filter.brand"), icon=":material/sell:", use_container_width=True):
        marcas_sel = st.multiselect(
            t("filter.brand.select"),
            marcas_opts,
            default=[],
            key="f_marca",
            placeholder=t("filter.brand.placeholder"),
        )

with f2:
    with st.popover(t("filter.gender"), icon=":material/person:", use_container_width=True):
        generos_sel = st.multiselect(
            t("filter.gender.select"),
            generos_opts,
            default=generos_opts,
            key="f_genero",
        )

with f3:
    with st.popover(t("filter.season"), icon=":material/calendar_month:", use_container_width=True):
        temporadas_sel = st.multiselect(
            t("filter.season.select"),
            temporadas_opts,
            default=temporadas_opts,
            key="f_temp",
        )

with f4:
    with st.popover(t("filter.price"), icon=":material/payments:", use_container_width=True):
        preco_range = st.slider(
            t("filter.price.label"),
            min_value=float(round(preco_min, 0)),
            max_value=float(round(preco_max, 0)),
            value=(float(round(preco_min, 0)), float(round(preco_max, 0))),
            step=10.0,
            key="f_preco",
        )

with f5:
    with st.popover(t("filter.rating"), icon=":material/star:", use_container_width=True):
        nota_min = st.slider(t("filter.rating"), 0.0, 5.0, 0.0, 0.5, key="f_nota")

with f6:
    if st.button(t("filter.clear"), use_container_width=True, key="reset_filters"):
        for k in ["f_marca", "f_genero", "f_temp", "f_preco", "f_nota"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

# Resumo dos filtros ativos
chips = []
if marcas_sel:
    chips.append(f"{len(marcas_sel)} {t('filter.brand').lower()}")
if len(generos_sel) < len(generos_opts):
    chips.append(f"{len(generos_sel)} {t('filter.gender').lower()}")
if len(temporadas_sel) < len(temporadas_opts):
    chips.append(f"{len(temporadas_sel)} {t('filter.season').lower()}")
if preco_range != (round(preco_min, 0), round(preco_max, 0)):
    chips.append(f"R$ {preco_range[0]:.0f}–R$ {preco_range[1]:.0f}")
if nota_min > 0:
    chips.append(f"≥ {nota_min:.1f}★")

if chips:
    st.markdown(
        f"<div class='filter-summary'>{t('filter.summary.active')}"
        + " · ".join([f"<span>{c}</span>" for c in chips])
        + "</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"<div class='filter-summary muted'>{t('filter.summary.none')}</div>",
        unsafe_allow_html=True,
    )

# Aplicar filtros
mask = (
    df["Gênero"].isin(generos_sel)
    & df["Temporada"].isin(temporadas_sel)
    & df["Preço"].between(preco_range[0], preco_range[1])
    & (df["Nota"] >= nota_min)
)
if marcas_sel:
    mask &= df["Marca"].isin(marcas_sel)

filtered = df[mask].copy()

if filtered.empty:
    st.warning(t("filter.empty"))
    footer()
    st.stop()

m = kpis(filtered)

kpi_grid([
    kpi_card(t("overview.kpi.slice"), f"{m['total']:,}".replace(",", "."),
             trend=t("overview.kpi.slice.trend.tpl", f"{m['total']/len(df)*100:.1f}")),
    kpi_card(t("overview.kpi.brands"), f"{m['marcas']}"),
    kpi_card(t("home.kpi.rating"), f"{m['nota_media']:.2f}", unit="/5"),
    kpi_card(t("home.kpi.ticket"), f"R$ {m['preco_medio']:.0f}",
             trend=t("home.kpi.ticket.trend.tpl", f"{m['preco_mediano']:.0f}")),
])

section_header(
    eyebrow=t("overview.section.composition.eyebrow"),
    title=t("overview.section.composition.title"),
    subtitle=t("overview.section.composition.subtitle"),
)

c1, c2 = st.columns([1.1, 1])
with c1:
    chart_title(t("overview.chart.brands.title"), t("overview.chart.brands.sub"))
    st.plotly_chart(bar_top_marcas(filtered, n=10), use_container_width=True, config=PLOTLY_CHART_CONFIG)
with c2:
    chart_title(t("overview.chart.ratings.title"), t("overview.chart.ratings.sub"))
    st.plotly_chart(hist_notas(filtered), use_container_width=True, config=PLOTLY_CHART_CONFIG)

top_brand = filtered["Marca"].value_counts().head(1)
if len(top_brand) > 0:
    nome = top_brand.index[0]
    qt = int(top_brand.iloc[0])
    insight_box(
        f"<strong>{nome}</strong> — <strong>{qt}</strong> "
        f"({qt/len(filtered)*100:.1f}%) · "
        f"{filtered[filtered['Marca']==nome]['Nota'].mean():.2f}/5",
        label=t("analysis.read"),
    )

section_header(
    eyebrow=t("overview.section.detail.eyebrow"),
    title=t("overview.section.detail.title"),
    subtitle=t("overview.section.detail.subtitle"),
)

display = (
    filtered.sort_values("N_Avaliações", ascending=False, na_position="last")
    [["Título", "Marca", "Gênero", "Temporada", "Material", "Nota", "N_Avaliações", "Preço"]]
    .head(50)
    .copy()
)
display["Preço"] = display["Preço"].apply(lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
display["Nota"] = display["Nota"].apply(lambda v: f"{v:.1f}")
display["N_Avaliações"] = display["N_Avaliações"].fillna(0).astype(int)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Título": st.column_config.TextColumn(t("table.col.product"), width="large"),
        "Marca": st.column_config.TextColumn(t("table.col.brand")),
        "Gênero": st.column_config.TextColumn(t("table.col.gender")),
        "Temporada": st.column_config.TextColumn(t("table.col.season")),
        "Material": st.column_config.TextColumn(t("table.col.material")),
        "Nota": st.column_config.TextColumn(t("table.col.rating")),
        "N_Avaliações": st.column_config.NumberColumn(t("table.col.reviews"), format="%d"),
        "Preço": st.column_config.TextColumn(t("table.col.price")),
    },
)

footer()
