from pathlib import Path
import pandas as pd
import streamlit as st

_CSV_PATH = Path(__file__).parent.parent / "ecommerce_preparados.csv"

GENEROS_VALIDOS = {
    "Bebês",
    "Feminino",
    "Masculino",
    "Meninas",
    "Meninos",
    "Sem gênero",
    "Sem gênero infantil",
    "Unissex",
}

TEMPORADAS_MAP = {
    "primavera/verão": "Primavera/Verão",
    "primavera-verão": "Primavera/Verão",
    "primavera/verão outono/inverno": "Atemporal",
    "primavera-verão outono-inverno": "Atemporal",
    "primavera-verão - outono-inverno": "Atemporal",
    "primavera/verão/outono/inverno": "Atemporal",
    "outono/inverno": "Outono/Inverno",
    "não definido": "Sem temporada",
    "2021": "Sem temporada",
}


def _clean_genero(v: str) -> str:
    if v in GENEROS_VALIDOS:
        return v
    return "Outros"


def _clean_temporada(v: str) -> str:
    return TEMPORADAS_MAP.get(v.strip().lower(), TEMPORADAS_MAP.get(v, "Sem temporada"))


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(_CSV_PATH)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df["Marca"] = df["Marca"].fillna("Sem marca").astype(str).str.strip()
    df["Material"] = df["Material"].fillna("não informado").astype(str).str.strip().str.lower()
    df["Gênero"] = df["Gênero"].fillna("Sem gênero").astype(str).str.strip().apply(_clean_genero)
    df["Temporada"] = df["Temporada"].fillna("não definido").astype(str).str.strip().apply(_clean_temporada)

    df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
    df["Nota"] = pd.to_numeric(df["Nota"], errors="coerce")
    df["N_Avaliações"] = pd.to_numeric(df["N_Avaliações"], errors="coerce")
    df["Desconto"] = pd.to_numeric(df["Desconto"], errors="coerce").fillna(0.0)

    def parse_qtd(v):
        if pd.isna(v):
            return None
        s = str(v).replace("+", "").replace(".", "").strip()
        try:
            return int(s)
        except ValueError:
            return None

    df["Qtd_Vendidos_Num"] = df["Qtd_Vendidos"].apply(parse_qtd)

    df = df.dropna(subset=["Preço", "Nota"]).reset_index(drop=True)

    return df


def kpis(df: pd.DataFrame) -> dict:
    return {
        "total": len(df),
        "marcas": df["Marca"].nunique(),
        "nota_media": float(df["Nota"].mean()),
        "preco_medio": float(df["Preço"].mean()),
        "preco_mediano": float(df["Preço"].median()),
        "avaliacoes_total": int(df["N_Avaliações"].fillna(0).sum()),
    }
