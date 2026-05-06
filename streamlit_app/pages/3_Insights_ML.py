import re
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from utils.theme import (
    page_setup,
    section_header,
    footer,
    insight_box,
    kpi_card,
    kpi_grid,
    chart_title,
    PLOTLY_CHART_CONFIG,
)
from utils.data_loader import load_data
from utils.charts import (
    feature_importance_bar,
    review_positivos_bar,
    review_negativos_bar,
)
from utils.i18n import t, language_selector

page_setup(t("nav.ml"), icon="🤖")

language_selector()

df = load_data()

# Hero narrativo
st.markdown(
    f"""
    <div class="ml-lab-band">
        <div class="ml-lab-band-inner">
            <div class="ml-lab-kicker">{t("ml.lab.kicker")}</div>
            <h1 class="ml-lab-title">{t("ml.lab.title")}</h1>
            <p class="ml-lab-copy">{t("ml.lab.copy")}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

section_header(
    eyebrow=t("ml.section1.eyebrow"),
    title=t("ml.section1.title"),
    subtitle=t("ml.section1.subtitle"),
)

FEATURE_COLS = ["Marca_Cod", "Material_Cod", "Temporada_Cod", "Nota", "N_Avaliações", "Desconto"]
GENERO_COLS_PREFIX = "Gen_"


@st.cache_resource(show_spinner="Treinando o Random Forest…")
def train_model(version: int = 3):
    base = load_data()
    base = base.dropna(subset=["Preço", "Marca_Cod", "Material_Cod", "Temporada_Cod"]).copy()
    base["N_Avaliações"] = base["N_Avaliações"].fillna(base["N_Avaliações"].median())
    base["Desconto"] = base["Desconto"].fillna(0.0)
    base = base[base["Preço"] <= base["Preço"].quantile(0.97)]

    gen_dummies = pd.get_dummies(base["Gênero"], prefix=GENERO_COLS_PREFIX.rstrip("_"))
    X = pd.concat([base[FEATURE_COLS].reset_index(drop=True), gen_dummies.reset_index(drop=True)], axis=1)
    y = base["Preço"].reset_index(drop=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=120, max_depth=14, min_samples_leaf=2, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    return {
        "model": model,
        "feature_names": X.columns.tolist(),
        "gen_columns": gen_dummies.columns.tolist(),
        "metrics": {"mae": mean_absolute_error(y_test, pred), "r2": r2_score(y_test, pred), "n_train": len(X_train), "n_test": len(X_test)},
        "marca_map": dict(zip(base["Marca"], base["Marca_Cod"])),
        "material_map": dict(zip(base["Material"], base["Material_Cod"])),
        "temporada_map": dict(zip(base["Temporada"], base["Temporada_Cod"])),
        "ranges": {
            "preco_median": float(base["Preço"].median()),
        },
    }


bundle = train_model()
metrics = bundle["metrics"]

kpi_grid([
    kpi_card(t("ml.kpi.mae"), f"R$ {metrics['mae']:.2f}", trend=t("ml.kpi.mae.trend")),
    kpi_card(t("ml.kpi.r2"), f"{metrics['r2']:.3f}", trend=t("ml.kpi.r2.trend")),
    kpi_card(t("ml.kpi.train"), f"{metrics['n_train']:,}".replace(",", "."), trend=t("ml.kpi.train.trend")),
    kpi_card(t("ml.kpi.test"), f"{metrics['n_test']:,}".replace(",", "."), trend=t("ml.kpi.test.trend")),
])

section_header(
    eyebrow=t("ml.sim.eyebrow"),
    title=t("ml.sim.title"),
    subtitle=t("ml.sim.subtitle"),
)

form_col, result_col = st.columns([1.15, 1], gap="large")

with form_col:
    marcas = sorted(bundle["marca_map"].keys())
    materiais = sorted(bundle["material_map"].keys())
    temporadas = sorted(bundle["temporada_map"].keys())
    generos = bundle["gen_columns"]

    with st.container(key="ml_calc_card"):
        st.markdown(f"<div class='ml-form-eyebrow'>{t('ml.form.eyebrow')}</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            marca_in = st.selectbox(t("filter.brand"), marcas, index=marcas.index("lupo") if "lupo" in marcas else 0)
            material_in = st.selectbox(t("table.col.material"), materiais, index=0)
            temporada_in = st.selectbox(t("filter.season"), temporadas, index=0)
        with c2:
            genero_in = st.selectbox(t("filter.gender"), [g.replace("Gen_", "") for g in generos], index=0)
            nota_in = st.slider(t("ml.form.expected_rating"), 1.0, 5.0, 4.5, 0.1)
            avaliacoes_in = st.slider(t("ml.form.review_volume"), 0, 5000, 200, 50)
        desconto_in = st.slider(t("ml.form.discount"), 0, 90, 10, 5)

        submit = st.button(t("ml.form.submit"), use_container_width=True, key="ml_submit", type="primary")

with result_col:
    if submit:
        x = {
            "Marca_Cod": bundle["marca_map"].get(marca_in, 0),
            "Material_Cod": bundle["material_map"].get(material_in, 0),
            "Temporada_Cod": bundle["temporada_map"].get(temporada_in, 0),
            "Nota": nota_in,
            "N_Avaliações": avaliacoes_in,
            "Desconto": float(desconto_in),
        }
        for g in generos:
            x[g] = 1 if g == f"Gen_{genero_in}" else 0

        x_df = pd.DataFrame([x])[bundle["feature_names"]]
        tree_preds = np.array([tr.predict(x_df.values)[0] for tr in bundle["model"].estimators_])
        preco_est = float(tree_preds.mean())
        p10, p90 = np.percentile(tree_preds, [10, 90])

        delta_pct = (preco_est / bundle["ranges"]["preco_median"] - 1) * 100
        position_key = "ml.result.position.above.tpl" if delta_pct >= 0 else "ml.result.position.below.tpl"
        position_text = t(position_key, f"{bundle['ranges']['preco_median']:.0f}", f"{abs(delta_pct):.1f}")

        st.markdown(
            f"""
            <div class="price-result">
                <div class="label">{t('ml.result.label')}</div>
                <div class="value">R$ {preco_est:.0f}</div>
                <div class="range">{t('ml.result.range.tpl', f'{p10:.0f}', f'{p90:.0f}')}</div>
                <div class="position">{position_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="ml-waiting-card">
                <div class="ml-waiting-icon">✦</div>
                <div class="ml-waiting-title">{t('ml.waiting.title')}</div>
                <div class="ml-waiting-body">{t('ml.waiting.body')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Feature importance
section_header(
    eyebrow=t("ml.feat.eyebrow"),
    title=t("ml.feat.title"),
    subtitle=t("ml.feat.subtitle"),
)

importances = bundle["model"].feature_importances_
feat_names = bundle["feature_names"]
labels = {
    "Marca_Cod": t("filter.brand"),
    "Material_Cod": t("table.col.material"),
    "Temporada_Cod": t("filter.season"),
    "Nota": t("home.kpi.rating"),
    "N_Avaliações": t("table.col.reviews"),
    "Desconto": t("ml.form.discount"),
}
pretty = []
for f in feat_names:
    if f.startswith(GENERO_COLS_PREFIX):
        pretty.append(f"{t('filter.gender')}: " + f.replace(GENERO_COLS_PREFIX, ""))
    else:
        pretty.append(labels.get(f, f))

agg = pd.DataFrame({"feat": pretty, "imp": importances})
gen_mask = agg["feat"].str.startswith(t("filter.gender") + ":")
gen_total = agg[gen_mask]["imp"].sum()
agg = agg[~gen_mask]
agg = pd.concat([agg, pd.DataFrame([{"feat": t("filter.gender"), "imp": gen_total}])], ignore_index=True)
agg = agg.sort_values("imp", ascending=False).head(8)

chart_title(t("ml.feat.chart.title"), t("ml.feat.chart.sub"))
st.plotly_chart(
    feature_importance_bar(agg["feat"].tolist(), agg["imp"].tolist()),
    use_container_width=True,
    config=PLOTLY_CHART_CONFIG,
)

top_feat = agg.iloc[0]
insight_box(
    f"<strong>{top_feat['feat']}</strong> · <strong>{top_feat['imp']*100:.1f}%</strong>",
    label=t("ml.feat.eyebrow"),
)

# === Voz do cliente ===
section_header(
    eyebrow=t("ml.section2.eyebrow"),
    title=t("ml.section2.title"),
    subtitle=t("ml.section2.subtitle"),
)


@st.cache_data(show_spinner=False)
def review_sentiment(version: int = 2):
    _df = load_data()
    pos_words = [
        "ótimo", "otimo", "excelente", "perfeito", "lindo", "lindas", "lindos",
        "confortável", "confortavel", "macio", "qualidade", "recomendo",
        "satisfeito", "satisfeita", "bom", "bons", "boa", "boas", "amei",
        "adorei", "maravilhoso", "maravilhosa", "vale", "barato",
    ]
    neg_words = [
        "ruim", "péssimo", "pessimo", "horrível", "horrivel", "decepção",
        "decepcao", "rasgou", "furou", "furo", "defeito", "pequeno",
        "apertado", "apertada", "fino", "fina", "frágil", "fragil",
        "não recomendo", "nao recomendo", "estraga", "desconfortável", "desconfortavel",
    ]

    text_blob = (
        _df["Review1"].fillna("").astype(str) + " "
        + _df["Review2"].fillna("").astype(str) + " "
        + _df["Review3"].fillna("").astype(str)
    ).str.lower()
    full = " ".join(text_blob.tolist())

    pos_counts = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", full)) for w in pos_words}
    pos_counts = {w: c for w, c in pos_counts.items() if c > 0}
    neg_counts = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", full)) for w in neg_words}
    neg_counts = {w: c for w, c in neg_counts.items() if c > 0}
    total_reviews = (text_blob.str.len() > 5).sum()
    return pos_counts, neg_counts, int(total_reviews)


pos_counts, neg_counts, total_reviews = review_sentiment()

pos_total = sum(pos_counts.values())
neg_total = sum(neg_counts.values())
ratio = pos_total / max(neg_total, 1)

kpi_grid([
    kpi_card(t("ml.kpi.reviews"), f"{total_reviews:,}".replace(",", ".")),
    kpi_card(t("ml.kpi.pos"), f"{pos_total:,}".replace(",", ".")),
    kpi_card(t("ml.kpi.neg"), f"{neg_total:,}".replace(",", ".")),
    kpi_card(t("ml.kpi.ratio"), f"{ratio:.1f}×", trend=t("ml.kpi.ratio.trend")),
])

c1, c2 = st.columns(2, gap="large")
with c1:
    chart_title(t("ml.chart.pos.title"), t("ml.chart.pos.sub"))
    st.plotly_chart(review_positivos_bar(pos_counts), use_container_width=True, config=PLOTLY_CHART_CONFIG)

with c2:
    chart_title(t("ml.chart.neg.title"), t("ml.chart.neg.sub"))
    st.plotly_chart(review_negativos_bar(neg_counts), use_container_width=True, config=PLOTLY_CHART_CONFIG)

if pos_counts and neg_counts:
    top_pos = max(pos_counts, key=pos_counts.get)
    top_neg = max(neg_counts, key=neg_counts.get)
    insight_box(
        f"<strong>“{top_pos}”</strong> · {pos_counts[top_pos]} · "
        f"<strong>“{top_neg}”</strong> · {neg_counts[top_neg]}",
        label=t("ml.section2.title"),
    )

footer()
