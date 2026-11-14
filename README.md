# Moda em Dados — site estático

Versão publicada em <https://moda.allefyrafael.codes> (Azure Static Web Apps, plano Free). Reproduz as
quatro páginas do app Streamlit (`streamlit_app/`) sem servidor Python: os gráficos usam Plotly.js e
o Random Forest roda no navegador.

## Como funciona

| Parte | Origem |
| --- | --- |
| `data/products.json` | CSV limpo por `streamlit_app/utils/data_loader.py` (1.407 produtos) |
| `data/analysis.json` | Dados dos cinco gráficos da Análise Exploratória |
| `data/model.json` | As 120 árvores do `RandomForestRegressor` treinado como em `pages/3_Insights_ML.py` |
| `data/reviews.json` | Contagem de termos positivos e negativos dos reviews |
| `data/i18n.json` | Textos PT/EN/ES de `streamlit_app/utils/i18n.py` |
| `js/forest.js` | Avaliação das árvores (comparação em float32, como o scikit-learn) |
| `vendor/plotly-cartesian-2.35.2.min.js` | Plotly.js (pacote cartesiano), servido pelo próprio site |

## Regenerar os dados

```bash
pip install "scikit-learn==1.5.2" "pandas==2.2.3" "numpy==2.1.3"
python tools/build_static.py
python tools/check_model_parity.py   # exige Node.js; compara o navegador com o scikit-learn
```

## Rodar localmente

```bash
python -m http.server 8720 --directory web
```

## Publicação

O workflow `.github/workflows/azure-static-web-apps.yml` publica a pasta `web/` a cada push em `main`
usando o secret `AZURE_STATIC_WEB_APPS_API_TOKEN`.

### Cópia de continuidade

O workflow `.github/workflows/pages-backup.yml` publica a mesma pasta no GitHub Pages depois que
o workflow da Azure termina com sucesso em `main`. Ele também pode ser executado manualmente. Antes
de enviar, regenera os JSONs e compara as previsões do navegador com o scikit-learn. O site usa
caminhos relativos e pode abrir no endereço do projeto no GitHub Pages, sem alterar
`moda.allefyrafael.codes`.

Para uma eventual troca de hospedagem: conferir as cinco páginas, PT/EN/ES, filtros, gráficos e
previsões na cópia; associar o domínio no GitHub Pages; mudar somente o CNAME `moda` e verificar
HTTPS. O retorno é restaurar o CNAME anterior enquanto a assinatura Azure estiver ativa.
