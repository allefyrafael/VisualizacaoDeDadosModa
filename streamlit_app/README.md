# Moda em Dados — Streamlit App

Dashboard editorial sobre 2.199 produtos do e-commerce brasileiro de moda. Reúne análise exploratória interativa, dashboard com filtros e dois modelos de machine learning (estimador de preço e análise de sentimento dos reviews).

## Rodar localmente

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

O app abre em `http://localhost:8501`.

## Deploy no Streamlit Community Cloud

1. Suba esta pasta (`streamlit_app/`) para um repositório público no GitHub. O CSV `ecommerce_preparados.csv` precisa estar incluído no repositório.
2. Acesse https://share.streamlit.io e clique em **New app**.
3. Conecte sua conta GitHub e selecione o repositório.
4. Em **Main file path**, informe `streamlit_app/app.py` (ou apenas `app.py` se a pasta for a raiz).
5. Clique em **Deploy**. O Streamlit Cloud instala as dependências do `requirements.txt` automaticamente.

## Estrutura

| Pasta / arquivo | Função |
|---|---|
| `app.py` | Home / landing page |
| `pages/1_Visao_Geral.py` | Dashboard com filtros dinâmicos |
| `pages/2_Analise_Exploratoria.py` | 5 gráficos exigidos pelo M10 (dispersão, calor, barra, pizza, densidade) |
| `pages/3_Insights_ML.py` | Random Forest (preço) + análise de termos em reviews |
| `pages/4_Sobre.py` | Bastidores e contatos |
| `utils/` | `data_loader`, `charts`, `theme` |
| `assets/style.css` | Identidade visual editorial |
| `.streamlit/config.toml` | Tema base do Streamlit |

## Stack

`streamlit` · `pandas` · `plotly` · `scikit-learn` · `numpy`
