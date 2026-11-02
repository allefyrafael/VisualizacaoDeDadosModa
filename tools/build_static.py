"""Gera os dados do site estático (web/data/*.json) a partir do app Streamlit.

Reaproveita a limpeza de `streamlit_app/utils/data_loader.py`, os textos de
`streamlit_app/utils/i18n.py` e o mesmo treino do Random Forest de
`streamlit_app/pages/3_Insights_ML.py`, sem precisar do Streamlit instalado.

Uso: python tools/build_static.py   (requer pandas, numpy e scikit-learn)
"""
from __future__ import annotations

import json
import re
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "streamlit_app"
OUT = ROOT / "web" / "data"


def _stub_streamlit() -> None:
    """Permite importar os módulos do app sem o Streamlit (só usamos funções puras)."""
    st = types.ModuleType("streamlit")
    st.cache_data = lambda *a, **k: (a[0] if a and callable(a[0]) else (lambda f: f))
    st.cache_resource = st.cache_data
    st.session_state = {}
    sys.modules["streamlit"] = st


_stub_streamlit()
sys.path.insert(0, str(APP))
from utils.data_loader import load_data, kpis  # noqa: E402
from utils.i18n import TRANSLATIONS  # noqa: E402

# Mesmos parâmetros de pages/3_Insights_ML.py
FEATURE_COLS = ["Marca_Cod", "Material_Cod", "Temporada_Cod", "Nota", "N_Avaliações", "Desconto"]
POS_WORDS = [
    "ótimo", "otimo", "excelente", "perfeito", "lindo", "lindas", "lindos",
    "confortável", "confortavel", "macio", "qualidade", "recomendo",
    "satisfeito", "satisfeita", "bom", "bons", "boa", "boas", "amei",
    "adorei", "maravilhoso", "maravilhosa", "vale", "barato",
]
NEG_WORDS = [
    "ruim", "péssimo", "pessimo", "horrível", "horrivel", "decepção",
    "decepcao", "rasgou", "furou", "furo", "defeito", "pequeno",
    "apertado", "apertada", "fino", "fina", "frágil", "fragil",
    "não recomendo", "nao recomendo", "estraga", "desconfortável", "desconfortavel",
]


def _clean(v):
    """NaN → None para JSON; floats com até 6 casas."""
    if v is None:
        return None
    if isinstance(v, (float, np.floating)):
        if np.isnan(v):
            return None
        return round(float(v), 6)
    if isinstance(v, (np.integer,)):
        return int(v)
    return v


def _markdown(text: str) -> str:
    """Markdown mínimo usado nos textos do app: **negrito**, *itálico*, listas e parágrafos."""
    def inline(s: str) -> str:
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"(?<![*<])\*(?!\*)(.+?)\*", r"<em>\1</em>", s)

    blocks = [b for b in text.split("\n\n") if b.strip()]
    out = []
    for b in blocks:
        lines = b.split("\n")
        if all(line.startswith("- ") for line in lines):
            out.append("<ul>" + "".join(f"<li>{inline(line[2:])}</li>" for line in lines) + "</ul>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "".join(out)


def build_i18n() -> dict:
    md_keys = {"about.motivation.body"}
    inline_md_keys = {k for k in TRANSLATIONS if k.startswith("home.card.") and k.endswith(".body")}
    out: dict[str, dict[str, str]] = {"pt": {}, "en": {}, "es": {}}
    for key, entry in TRANSLATIONS.items():
        for lang in out:
            text = entry.get(lang) or entry.get("pt") or key
            if key in md_keys:
                text = _markdown(text)
            elif key in inline_md_keys:
                text = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<em>\1</em>", text)
            out[lang][key] = text
    return out


def build_products(df: pd.DataFrame) -> list[dict]:
    cols = ["Título", "Marca", "Gênero", "Temporada", "Material", "Nota", "N_Avaliações",
            "Preço", "Desconto", "Qtd_Vendidos_Num"]
    rows = []
    for rec in df[cols].to_dict("records"):
        rows.append({
            "t": rec["Título"], "b": rec["Marca"], "g": rec["Gênero"], "s": rec["Temporada"],
            "m": rec["Material"], "r": _clean(rec["Nota"]), "n": _clean(rec["N_Avaliações"]),
            "p": _clean(rec["Preço"]), "d": _clean(rec["Desconto"]),
            "q": _clean(rec["Qtd_Vendidos_Num"]),
        })
    return rows


def build_analysis(df: pd.DataFrame) -> dict:
    """Dados dos gráficos da Análise Exploratória (catálogo completo, sem filtros)."""
    base = df.dropna(subset=["Preço", "N_Avaliações", "Nota"]).copy()
    base = base[base["Preço"] <= base["Preço"].quantile(0.97)]
    base = base[base["N_Avaliações"] <= base["N_Avaliações"].quantile(0.97)]
    scatter = {
        "x": base["N_Avaliações"].tolist(),
        "y": base["Preço"].tolist(),
        "rating": base["Nota"].tolist(),
        "size": base["Qtd_Vendidos_Num"].fillna(50).clip(lower=10, upper=2000).tolist(),
        "brand": base["Marca"].tolist(),
        "gender": base["Gênero"].tolist(),
        "season": base["Temporada"].tolist(),
    }

    corr_cols = ["Nota", "N_Avaliações", "Desconto", "Preço", "Qtd_Vendidos_Num"]
    corr = df[corr_cols].corr().round(2)

    vbase = df.dropna(subset=["Preço", "Temporada"]).copy()
    vbase = vbase[vbase["Preço"] <= vbase["Preço"].quantile(0.95)]
    order = vbase.groupby("Temporada")["Preço"].median().sort_values().index.tolist()
    violins = [
        {"name": temp, "y": vbase[vbase["Temporada"] == temp]["Preço"].tolist()}
        for temp in order
        if len(vbase[vbase["Temporada"] == temp]) >= 5
    ]

    pop = df.dropna(subset=["N_Avaliações", "Preço"])
    top_pop = pop.nlargest(50, "N_Avaliações")
    top1 = df["Marca"].value_counts().head(1)
    g = df["Gênero"].value_counts(normalize=True) * 100
    medians = df.groupby("Temporada")["Preço"].median().sort_values(ascending=False)
    gender_counts = df["Gênero"].value_counts()

    return {
        "scatter": scatter,
        "corr": {"cols": corr_cols, "z": corr.values.tolist()},
        "violins": violins,
        "genders": {"labels": gender_counts.index.tolist(), "values": gender_counts.values.tolist()},
        "insights": {
            "q1": {"mean": float(top_pop["Preço"].mean()),
                   "delta": float((top_pop["Preço"].mean() / df["Preço"].mean() - 1) * 100)},
            "q2": {"qa": float(df[["N_Avaliações", "Qtd_Vendidos_Num"]].corr().iloc[0, 1]),
                   "pn": float(df[["Preço", "Nota"]].corr().iloc[0, 1])},
            "q3": {"brand": top1.index[0], "count": int(top1.iloc[0]), "pct": float(top1.iloc[0] / len(df) * 100)},
            "q4": {"gender": g.index[0], "pct": float(g.iloc[0])},
            "q5": {"top": medians.index[0], "top_price": float(medians.iloc[0]),
                   "bottom": medians.index[-1], "bottom_price": float(medians.iloc[-1])},
        },
    }


def train_model(df: pd.DataFrame):
    base = df.dropna(subset=["Preço", "Marca_Cod", "Material_Cod", "Temporada_Cod"]).copy()
    base["N_Avaliações"] = base["N_Avaliações"].fillna(base["N_Avaliações"].median())
    base["Desconto"] = base["Desconto"].fillna(0.0)
    base = base[base["Preço"] <= base["Preço"].quantile(0.97)]

    gen_dummies = pd.get_dummies(base["Gênero"], prefix="Gen")
    X = pd.concat([base[FEATURE_COLS].reset_index(drop=True), gen_dummies.reset_index(drop=True)], axis=1)
    y = base["Preço"].reset_index(drop=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=120, max_depth=14, min_samples_leaf=2, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return model, X, base, gen_dummies, {
        "mae": float(mean_absolute_error(y_test, pred)),
        "r2": float(r2_score(y_test, pred)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }


def export_tree(est) -> list:
    """Árvore em arrays paralelos: feature (negativa = folha), limiar, filho esq./dir., valor."""
    tr = est.tree_
    return [
        tr.feature.tolist(),
        [float(v) for v in tr.threshold],  # precisão total: a comparação é feita em float32
        tr.children_left.tolist(),
        tr.children_right.tolist(),
        [round(float(v), 6) for v in tr.value[:, 0, 0]],
    ]


def build_model(df: pd.DataFrame) -> tuple[dict, dict]:
    model, X, base, gen_dummies, metrics = train_model(df)
    payload = {
        "features": X.columns.tolist(),
        "gen_columns": gen_dummies.columns.tolist(),
        "metrics": metrics,
        "importances": [float(v) for v in model.feature_importances_],
        "marca_map": {k: _clean(v) for k, v in zip(base["Marca"], base["Marca_Cod"])},
        "material_map": {k: _clean(v) for k, v in zip(base["Material"], base["Material_Cod"])},
        "temporada_map": {k: _clean(v) for k, v in zip(base["Temporada"], base["Temporada_Cod"])},
        "preco_median": float(base["Preço"].median()),
        "trees": [export_tree(est) for est in model.estimators_],
    }
    return payload, {"model": model, "X": X}


def build_reviews(df: pd.DataFrame) -> dict:
    text_blob = (
        df["Review1"].fillna("").astype(str) + " "
        + df["Review2"].fillna("").astype(str) + " "
        + df["Review3"].fillna("").astype(str)
    ).str.lower()
    full = " ".join(text_blob.tolist())
    pos = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", full)) for w in POS_WORDS}
    neg = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", full)) for w in NEG_WORDS}
    return {
        "pos": {w: c for w, c in pos.items() if c > 0},
        "neg": {w: c for w, c in neg.items() if c > 0},
        "total_reviews": int((text_blob.str.len() > 5).sum()),
    }


def write(name: str, data) -> None:
    path = OUT / name
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{name}: {path.stat().st_size / 1024:.0f} KB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_data()
    m = kpis(df)
    write("i18n.json", build_i18n())
    write("products.json", {"kpis": m, "rows": build_products(df)})
    write("analysis.json", build_analysis(df))
    write("reviews.json", build_reviews(df))
    model_payload, _ = build_model(df)
    write("model.json", model_payload)


if __name__ == "__main__":
    main()
