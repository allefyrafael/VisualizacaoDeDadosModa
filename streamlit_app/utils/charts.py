import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .theme import COLORS, PALETTE, PLOTLY_LAYOUT


def _apply_layout(fig: go.Figure, height: int = 460) -> go.Figure:
    """Aplica layout base SEM título Plotly (títulos vão para HTML acima do chart)."""
    layout = dict(PLOTLY_LAYOUT)
    margin = dict(layout.get("margin") or {})
    margin["t"] = 30
    margin["r"] = 24
    margin["l"] = 16
    margin["b"] = 48
    layout["margin"] = margin
    fig.update_layout(**layout)
    fig.update_layout(
        height=height,
        title=dict(text=""),
        modebar=dict(
            orientation="h",
            bgcolor="rgba(250,247,242,0.0)",
            activecolor=COLORS["primary"],
            color=COLORS["muted"],
        ),
    )
    return fig


def scatter_preco_avaliacoes(df: pd.DataFrame) -> go.Figure:
    base = df.dropna(subset=["Preço", "N_Avaliações", "Nota"]).copy()
    base = base[base["Preço"] <= base["Preço"].quantile(0.97)]
    base = base[base["N_Avaliações"] <= base["N_Avaliações"].quantile(0.97)]

    fig = px.scatter(
        base,
        x="N_Avaliações",
        y="Preço",
        color="Nota",
        size=base["Qtd_Vendidos_Num"].fillna(50).clip(lower=10, upper=2000),
        hover_data={
            "Marca": True,
            "Gênero": True,
            "Temporada": True,
            "Nota": ":.1f",
            "Preço": ":.2f",
            "N_Avaliações": True,
        },
        color_continuous_scale=[
            (0.0, "#9CA3AF"),
            (0.5, COLORS["gold"]),
            (1.0, COLORS["primary"]),
        ],
        labels={"N_Avaliações": "Número de avaliações", "Preço": "Preço (R$)"},
    )
    fig.update_traces(marker=dict(line=dict(width=0.4, color="white"), opacity=0.78))
    return _apply_layout(fig, height=520)


def heatmap_corr(df: pd.DataFrame) -> go.Figure:
    cols = ["Nota", "N_Avaliações", "Desconto", "Preço", "Qtd_Vendidos_Num"]
    available = [c for c in cols if c in df.columns]
    corr = df[available].corr().round(2)
    labels = {
        "Nota": "Nota",
        "N_Avaliações": "Avaliações",
        "Desconto": "Desconto",
        "Preço": "Preço",
        "Qtd_Vendidos_Num": "Qtd. Vendidos",
    }
    pretty = [labels.get(c, c) for c in available]

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=pretty,
            y=pretty,
            colorscale=[
                [0.0, "#0891B2"],
                [0.5, "#FAF7F2"],
                [1.0, COLORS["primary"]],
            ],
            zmin=-1,
            zmax=1,
            text=corr.values,
            texttemplate="%{text:.2f}",
            textfont=dict(family="DM Sans, sans-serif", size=13, color=COLORS["ink"]),
            colorbar=dict(title="Correlação", thickness=14, outlinewidth=0),
        )
    )
    fig.update_layout(xaxis=dict(side="bottom"))
    return _apply_layout(fig, height=480)


def bar_top_marcas(df: pd.DataFrame, n: int = 10) -> go.Figure:
    counts = (
        df["Marca"]
        .value_counts()
        .head(n)
        .sort_values(ascending=True)
        .reset_index()
    )
    counts.columns = ["Marca", "Produtos"]

    fig = px.bar(
        counts,
        x="Produtos",
        y="Marca",
        orientation="h",
        text="Produtos",
        color="Produtos",
        color_continuous_scale=[
            (0.0, COLORS["gold"]),
            (1.0, COLORS["primary"]),
        ],
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(family="DM Sans, sans-serif", size=12, color=COLORS["ink"]),
        hovertemplate="<b>%{y}</b><br>%{x} produtos<extra></extra>",
        cliponaxis=False,
    )
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Produtos no catálogo")
    return _apply_layout(fig, height=520)


def pie_genero(df: pd.DataFrame) -> go.Figure:
    counts = df["Gênero"].value_counts().reset_index()
    counts.columns = ["Gênero", "Produtos"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts["Gênero"],
                values=counts["Produtos"],
                hole=0.55,
                marker=dict(
                    colors=PALETTE[: len(counts)],
                    line=dict(color="white", width=3),
                ),
                textinfo="label+percent",
                textfont=dict(family="DM Sans, sans-serif", size=13, color=COLORS["ink"]),
                hovertemplate="<b>%{label}</b><br>%{value} produtos (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        annotations=[
            dict(
                text=f"<b style='font-family:Playfair Display'>{counts['Produtos'].sum()}</b><br><span style='font-size:11px;color:#9CA3AF;letter-spacing:1.5px;'>PRODUTOS</span>",
                x=0.5,
                y=0.5,
                font=dict(size=22, color=COLORS["ink"]),
                showarrow=False,
            )
        ],
        showlegend=False,
    )
    return _apply_layout(fig, height=480)


def density_preco_temporada(df: pd.DataFrame) -> go.Figure:
    base = df.dropna(subset=["Preço", "Temporada"]).copy()
    base = base[base["Preço"] <= base["Preço"].quantile(0.95)]

    order = (
        base.groupby("Temporada")["Preço"]
        .median()
        .sort_values()
        .index.tolist()
    )

    fig = go.Figure()
    for i, temp in enumerate(order):
        sub = base[base["Temporada"] == temp]["Preço"]
        if len(sub) < 5:
            continue
        fig.add_trace(
            go.Violin(
                y=sub,
                name=temp,
                box_visible=True,
                meanline_visible=True,
                fillcolor=PALETTE[i % len(PALETTE)],
                line_color=COLORS["ink"],
                opacity=0.75,
                points=False,
            )
        )
    fig.update_layout(
        yaxis_title="Preço (R$)",
        xaxis_title="",
        violinmode="group",
        showlegend=False,
    )
    return _apply_layout(fig, height=500)


def hist_notas(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="Nota",
        nbins=20,
        color_discrete_sequence=[COLORS["primary"]],
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="white")),
        opacity=0.85,
        hovertemplate="Nota: %{x}<br>%{y} produtos<extra></extra>",
    )
    media = df["Nota"].mean()
    fig.add_vline(
        x=media,
        line_dash="dash",
        line_color=COLORS["plum"],
        annotation_text=f"média {media:.2f}",
        annotation_position="top left",
        annotation_font_color=COLORS["plum"],
    )
    fig.update_layout(yaxis_title="Produtos", xaxis_title="Nota")
    return _apply_layout(fig, height=380)


def feature_importance_bar(features: list[str], importances: list[float]) -> go.Figure:
    df = (
        pd.DataFrame({"feat": features, "imp": importances})
        .sort_values("imp", ascending=True)
    )
    fig = px.bar(
        df,
        x="imp",
        y="feat",
        orientation="h",
        text=df["imp"].round(3),
        color="imp",
        color_continuous_scale=[(0, COLORS["gold"]), (1, COLORS["primary"])],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Importância relativa",
        yaxis_title="",
    )
    return _apply_layout(fig, height=440)


def review_positivos_bar(positive: dict, top_n: int = 10) -> go.Figure:
    items = sorted(positive.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    if not items:
        return _apply_layout(go.Figure(), height=380)
    df = pd.DataFrame(items, columns=["palavra", "menções"]).sort_values("menções", ascending=True)

    fig = px.bar(
        df,
        x="menções",
        y="palavra",
        orientation="h",
        text="menções",
        color_discrete_sequence=[COLORS["moss"]],
    )
    fig.update_traces(
        marker_line_width=0,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{x} menções<extra></extra>",
    )
    fig.update_layout(
        xaxis_title="Menções nos reviews",
        yaxis_title="",
        showlegend=False,
    )
    return _apply_layout(fig, height=420)


def review_negativos_bar(negative: dict, top_n: int = 10) -> go.Figure:
    items = sorted(negative.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    if not items:
        return _apply_layout(go.Figure(), height=380)
    df = pd.DataFrame(items, columns=["palavra", "menções"]).sort_values("menções", ascending=True)

    fig = px.bar(
        df,
        x="menções",
        y="palavra",
        orientation="h",
        text="menções",
        color_discrete_sequence=[COLORS["primary"]],
    )
    fig.update_traces(
        marker_line_width=0,
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{x} menções<extra></extra>",
    )
    fig.update_layout(
        xaxis_title="Menções nos reviews",
        yaxis_title="",
        showlegend=False,
    )
    return _apply_layout(fig, height=420)
