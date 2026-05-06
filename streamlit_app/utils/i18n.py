"""Sistema de internacionalização (PT/EN/ES) para o Moda em Dados."""
import streamlit as st

LANGUAGES = {
    "pt": {"label": "Português", "code": "PT", "flag": "🇧🇷"},
    "en": {"label": "English", "code": "EN", "flag": "🇺🇸"},
    "es": {"label": "Español", "code": "ES", "flag": "🇪🇸"},
}

# SVG flags inline — renderizam de forma consistente em qualquer SO
FLAG_SVGS = {
    "pt": (
        '<svg viewBox="0 0 24 16" width="24" height="16" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect width="24" height="16" fill="#009C3B"/>'
        '<path d="M12 3 L21 8 L12 13 L3 8 Z" fill="#FFDF00"/>'
        '<circle cx="12" cy="8" r="2.5" fill="#002776"/>'
        '<path d="M9.7 7.6 Q12 7 14.3 7.6" stroke="#FFFFFF" stroke-width="0.4" fill="none"/>'
        '</svg>'
    ),
    "en": (
        '<svg viewBox="0 0 24 16" width="24" height="16" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect width="24" height="16" fill="#B22234"/>'
        '<path d="M0 1.85h24M0 4.62h24M0 7.38h24M0 10.15h24M0 12.92h24" stroke="#FFFFFF" stroke-width="1.23"/>'
        '<rect width="10" height="8.6" fill="#3C3B6E"/>'
        '<g fill="#FFFFFF" font-size="2">'
        '<text x="1" y="2">★</text><text x="3.5" y="2">★</text><text x="6" y="2">★</text><text x="8.5" y="2">★</text>'
        '<text x="2.2" y="4">★</text><text x="4.8" y="4">★</text><text x="7.3" y="4">★</text>'
        '<text x="1" y="6">★</text><text x="3.5" y="6">★</text><text x="6" y="6">★</text><text x="8.5" y="6">★</text>'
        '<text x="2.2" y="8">★</text><text x="4.8" y="8">★</text><text x="7.3" y="8">★</text>'
        '</g>'
        '</svg>'
    ),
    "es": (
        '<svg viewBox="0 0 24 16" width="24" height="16" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect width="24" height="16" fill="#AA151B"/>'
        '<rect y="4" width="24" height="8" fill="#F1BF00"/>'
        '</svg>'
    ),
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ===== Navegação / Sidebar =====
    "nav.home": {"pt": "Home", "en": "Home", "es": "Inicio"},
    "nav.overview": {"pt": "Visão Geral", "en": "Overview", "es": "Vista General"},
    "nav.analysis": {"pt": "Análise Exploratória", "en": "Exploratory Analysis", "es": "Análisis Exploratorio"},
    "nav.ml": {"pt": "Insights com ML", "en": "ML Insights", "es": "Insights con ML"},
    "nav.about": {"pt": "Sobre", "en": "About", "es": "Acerca"},

    # ===== Home =====
    "home.title": {"pt": "Home", "en": "Home", "es": "Inicio"},
    "home.hero.eyebrow": {
        "pt": "Atelier de Dados · Edição 2026",
        "en": "Data Atelier · 2026 Edition",
        "es": "Atelier de Datos · Edición 2026",
    },
    "home.hero.title": {
        "pt": "Moda em <em>Dados</em>",
        "en": "Fashion in <em>Data</em>",
        "es": "Moda en <em>Datos</em>",
    },
    "home.hero.subtitle": {
        "pt": "Uma jornada visual e analítica por <strong>2.199 produtos</strong> do e-commerce brasileiro de moda — preços, marcas, avaliações e o que os consumidores realmente sentem em seus reviews.",
        "en": "A visual and analytical journey through <strong>2,199 products</strong> from Brazilian fashion e-commerce — prices, brands, ratings, and what customers actually feel in their reviews.",
        "es": "Un recorrido visual y analítico por <strong>2.199 productos</strong> del e-commerce brasileño de moda — precios, marcas, valoraciones y lo que los clientes realmente sienten en sus reseñas.",
    },
    "home.kpi.products": {"pt": "Produtos catalogados", "en": "Catalogued products", "es": "Productos catalogados"},
    "home.kpi.products.trend": {"pt": "dataset completo", "en": "complete dataset", "es": "dataset completo"},
    "home.kpi.brands": {"pt": "Marcas únicas", "en": "Unique brands", "es": "Marcas únicas"},
    "home.kpi.brands.trend": {"pt": "diversidade do catálogo", "en": "catalog diversity", "es": "diversidad del catálogo"},
    "home.kpi.rating": {"pt": "Nota média", "en": "Average rating", "es": "Calificación media"},
    "home.kpi.rating.trend": {"pt": "satisfação geral", "en": "overall satisfaction", "es": "satisfacción general"},
    "home.kpi.ticket": {"pt": "Ticket médio", "en": "Average ticket", "es": "Ticket medio"},
    "home.kpi.ticket.trend.tpl": {"pt": "mediana R$ {0}", "en": "median R$ {0}", "es": "mediana R$ {0}"},

    "home.manifesto.eyebrow": {"pt": "POR QUE ESTE PROJETO EXISTE", "en": "WHY THIS PROJECT EXISTS", "es": "POR QUÉ EXISTE ESTE PROYECTO"},
    "home.manifesto.lead": {
        "pt": "Notebooks ficam <em>presos</em> em PDFs e prints. Decisões reais nunca cabem em uma célula de Jupyter.",
        "en": "Notebooks get <em>trapped</em> in PDFs and screenshots. Real decisions never fit in a Jupyter cell.",
        "es": "Los notebooks quedan <em>atrapados</em> en PDFs y capturas. Las decisiones reales nunca caben en una celda de Jupyter.",
    },
    "home.manifesto.body": {
        "pt": "Este projeto nasceu para fechar a lacuna entre <strong>análise estática</strong> e <strong>produto navegável</strong>. Aplica princípios de <em>Storytelling with Data</em> (Cole Knaflic) — contexto antes do gráfico, menos ruído, hierarquia clara — e os combina com aprendizado de máquina para que qualquer pessoa, técnica ou não, consiga extrair valor de 2 mil produtos em segundos.",
        "en": "This project was born to close the gap between <strong>static analysis</strong> and <strong>navigable product</strong>. It applies principles from <em>Storytelling with Data</em> (Cole Knaflic) — context before the chart, less noise, clear hierarchy — and combines them with machine learning so anyone, technical or not, can extract value from 2,000 products in seconds.",
        "es": "Este proyecto nació para cerrar la brecha entre <strong>análisis estático</strong> y <strong>producto navegable</strong>. Aplica principios de <em>Storytelling with Data</em> (Cole Knaflic) — contexto antes del gráfico, menos ruido, jerarquía clara — y los combina con machine learning para que cualquier persona, técnica o no, pueda extraer valor de 2 mil productos en segundos.",
    },

    "home.acts.eyebrow": {"pt": "A história em três atos", "en": "The story in three acts", "es": "La historia en tres actos"},
    "home.acts.title": {"pt": "Da pergunta à decisão", "en": "From question to decision", "es": "De la pregunta a la decisión"},
    "home.acts.subtitle": {
        "pt": "Inspirado em Storytelling with Data — cada página existe para responder uma pergunta diferente. Entre na ordem ou pule direto ao que importa.",
        "en": "Inspired by Storytelling with Data — each page exists to answer a different question. Go in order or jump straight to what matters.",
        "es": "Inspirado en Storytelling with Data — cada página existe para responder una pregunta distinta. Entra en orden o salta directo a lo que importa.",
    },

    "home.card.dashboard.eyebrow": {"pt": "ATO 01 · DASHBOARD", "en": "ACT 01 · DASHBOARD", "es": "ACTO 01 · PANEL"},
    "home.card.dashboard.title": {"pt": "Visão Geral do catálogo", "en": "Catalog Overview", "es": "Vista General del catálogo"},
    "home.card.dashboard.body": {
        "pt": "Pergunta: *como anda o negócio agora?* KPIs vivos e ranking de marcas com filtros por gênero, temporada, faixa de preço e nota.",
        "en": "Question: *how is the business doing now?* Live KPIs and brand ranking with filters by gender, season, price range, and rating.",
        "es": "Pregunta: *¿cómo va el negocio ahora?* KPIs en vivo y ranking de marcas con filtros por género, temporada, rango de precio y calificación.",
    },
    "home.card.dashboard.cta": {"pt": "Acessar →", "en": "Open →", "es": "Abrir →"},

    "home.card.analysis.eyebrow": {"pt": "ATO 02 · ANÁLISE", "en": "ACT 02 · ANALYSIS", "es": "ACTO 02 · ANÁLISIS"},
    "home.card.analysis.title": {"pt": "Cinco perguntas, cinco respostas", "en": "Five questions, five answers", "es": "Cinco preguntas, cinco respuestas"},
    "home.card.analysis.body": {
        "pt": "Pergunta: *o que esses dados me dizem?* Cinco gráficos interativos com leitura editorial — dispersão, correlações, barras, pizza e densidade.",
        "en": "Question: *what do these data tell me?* Five interactive charts with editorial reading — scatter, correlations, bars, pie, and density.",
        "es": "Pregunta: *¿qué me dicen estos datos?* Cinco gráficos interactivos con lectura editorial — dispersión, correlaciones, barras, pastel y densidad.",
    },
    "home.card.analysis.cta": {"pt": "Acessar →", "en": "Open →", "es": "Abrir →"},

    "home.card.ml.eyebrow": {"pt": "ATO 03 · INTELIGÊNCIA", "en": "ACT 03 · INTELLIGENCE", "es": "ACTO 03 · INTELIGENCIA"},
    "home.card.ml.title": {"pt": "Da explicação à predição", "en": "From explanation to prediction", "es": "De la explicación a la predicción"},
    "home.card.ml.body": {
        "pt": "Pergunta: *o que tende a acontecer?* Random Forest estima preço de qualquer produto e a voz do cliente vira lista de oportunidades.",
        "en": "Question: *what is likely to happen?* Random Forest estimates the price of any product and the customer's voice becomes a list of opportunities.",
        "es": "Pregunta: *¿qué tiende a pasar?* Random Forest estima el precio de cualquier producto y la voz del cliente se vuelve lista de oportunidades.",
    },
    "home.card.ml.cta": {"pt": "Acessar →", "en": "Open →", "es": "Abrir →"},

    "home.dataset.eyebrow": {"pt": "Sobre o dataset", "en": "About the dataset", "es": "Sobre el dataset"},
    "home.dataset.title": {"pt": "O que esses dados nos contam", "en": "What this data tells us", "es": "Lo que estos datos nos cuentan"},
    "home.dataset.subtitle": {
        "pt": "Coleção completa de produtos de moda capturada de um marketplace brasileiro.",
        "en": "Complete collection of fashion products captured from a Brazilian marketplace.",
        "es": "Colección completa de productos de moda capturada de un marketplace brasileño.",
    },

    # ===== Visão Geral =====
    "overview.hero.eyebrow": {"pt": "01 · Dashboard", "en": "01 · Dashboard", "es": "01 · Panel"},
    "overview.hero.title": {
        "pt": "<em>Visão</em> geral do catálogo",
        "en": "Catalog <em>Overview</em>",
        "es": "<em>Vista</em> general del catálogo",
    },
    "overview.hero.subtitle": {
        "pt": "Filtre por marca, gênero, temporada, preço e nota mínima nos chips abaixo. Os indicadores e gráficos respondem em tempo real.",
        "en": "Filter by brand, gender, season, price, and minimum rating in the chips below. Indicators and charts respond in real time.",
        "es": "Filtra por marca, género, temporada, precio y calificación mínima en los chips de abajo. Los indicadores y gráficos responden en tiempo real.",
    },
    "filter.brand": {"pt": "Marca", "en": "Brand", "es": "Marca"},
    "filter.gender": {"pt": "Gênero", "en": "Gender", "es": "Género"},
    "filter.season": {"pt": "Temporada", "en": "Season", "es": "Temporada"},
    "filter.price": {"pt": "Faixa de preço", "en": "Price range", "es": "Rango de precio"},
    "filter.rating": {"pt": "Nota mínima", "en": "Minimum rating", "es": "Calificación mínima"},
    "filter.clear": {"pt": "Limpar", "en": "Clear", "es": "Limpiar"},
    "filter.brand.select": {"pt": "Selecione marcas", "en": "Select brands", "es": "Selecciona marcas"},
    "filter.brand.placeholder": {"pt": "Todas as marcas", "en": "All brands", "es": "Todas las marcas"},
    "filter.gender.select": {"pt": "Selecione gêneros", "en": "Select genders", "es": "Selecciona géneros"},
    "filter.season.select": {"pt": "Selecione temporadas", "en": "Select seasons", "es": "Selecciona temporadas"},
    "filter.price.label": {"pt": "Preço (R$)", "en": "Price (R$)", "es": "Precio (R$)"},
    "filter.summary.active": {"pt": "Filtros ativos: ", "en": "Active filters: ", "es": "Filtros activos: "},
    "filter.summary.none": {"pt": "Nenhum filtro aplicado · exibindo o catálogo completo", "en": "No filters applied · showing the complete catalog", "es": "Sin filtros aplicados · mostrando el catálogo completo"},
    "filter.empty": {"pt": "Nenhum produto atende a essa combinação. Suavize os filtros para continuar.", "en": "No product matches this combination. Loosen the filters to continue.", "es": "Ningún producto cumple esa combinación. Suaviza los filtros para continuar."},

    "overview.kpi.slice": {"pt": "Produtos no recorte", "en": "Products in slice", "es": "Productos en el corte"},
    "overview.kpi.slice.trend.tpl": {"pt": "{0}% do catálogo", "en": "{0}% of catalog", "es": "{0}% del catálogo"},
    "overview.kpi.brands": {"pt": "Marcas presentes", "en": "Brands present", "es": "Marcas presentes"},
    "overview.section.composition.eyebrow": {"pt": "Composição", "en": "Composition", "es": "Composición"},
    "overview.section.composition.title": {"pt": "Quem domina o recorte", "en": "Who dominates the slice", "es": "Quién domina el corte"},
    "overview.section.composition.subtitle": {
        "pt": "Volume de produtos por marca e distribuição de notas no conjunto filtrado.",
        "en": "Product volume by brand and rating distribution in the filtered set.",
        "es": "Volumen de productos por marca y distribución de calificaciones en el conjunto filtrado.",
    },
    "overview.chart.brands.title": {"pt": "Top 10 marcas por volume", "en": "Top 10 brands by volume", "es": "Top 10 marcas por volumen"},
    "overview.chart.brands.sub": {"pt": "Quem ocupa mais espaço no recorte filtrado.", "en": "Who occupies more space in the filtered slice.", "es": "Quién ocupa más espacio en el corte filtrado."},
    "overview.chart.ratings.title": {"pt": "Distribuição das notas", "en": "Ratings distribution", "es": "Distribución de calificaciones"},
    "overview.chart.ratings.sub": {"pt": "Onde se concentra a satisfação no recorte.", "en": "Where satisfaction concentrates in the slice.", "es": "Dónde se concentra la satisfacción en el corte."},
    "overview.section.detail.eyebrow": {"pt": "Detalhamento", "en": "Details", "es": "Detalle"},
    "overview.section.detail.title": {"pt": "Top produtos do recorte", "en": "Top products in the slice", "es": "Mejores productos del corte"},
    "overview.section.detail.subtitle": {
        "pt": "Ordenado por volume de avaliações. Use as colunas para reordenar.",
        "en": "Ordered by review volume. Use the columns to reorder.",
        "es": "Ordenado por volumen de reseñas. Usa las columnas para reordenar.",
    },
    "table.col.product": {"pt": "Produto", "en": "Product", "es": "Producto"},
    "table.col.brand": {"pt": "Marca", "en": "Brand", "es": "Marca"},
    "table.col.gender": {"pt": "Gênero", "en": "Gender", "es": "Género"},
    "table.col.season": {"pt": "Temporada", "en": "Season", "es": "Temporada"},
    "table.col.material": {"pt": "Material", "en": "Material", "es": "Material"},
    "table.col.rating": {"pt": "Nota", "en": "Rating", "es": "Calificación"},
    "table.col.reviews": {"pt": "Avaliações", "en": "Reviews", "es": "Reseñas"},
    "table.col.price": {"pt": "Preço", "en": "Price", "es": "Precio"},

    # ===== Análise =====
    "analysis.hero.eyebrow": {"pt": "02 · Análise · Storytelling com Dados", "en": "02 · Analysis · Storytelling with Data", "es": "02 · Análisis · Storytelling con Datos"},
    "analysis.hero.title": {
        "pt": "Cinco <em>perguntas</em>, cinco gráficos, cinco respostas",
        "en": "Five <em>questions</em>, five charts, five answers",
        "es": "Cinco <em>preguntas</em>, cinco gráficos, cinco respuestas",
    },
    "analysis.hero.subtitle": {
        "pt": "Inspirado nos princípios de Cole Knaflic em <em>Storytelling with Data</em>: cada visualização parte de uma <strong>pergunta de negócio</strong>, elimina o ruído visual e termina com uma <strong>leitura objetiva</strong> — não é gráfico bonito por estética, é gráfico que decide.",
        "en": "Inspired by Cole Knaflic's principles in <em>Storytelling with Data</em>: each visualization starts from a <strong>business question</strong>, eliminates visual noise, and ends with an <strong>objective reading</strong> — it's not a pretty chart for aesthetics, it's a chart that decides.",
        "es": "Inspirado en los principios de Cole Knaflic en <em>Storytelling with Data</em>: cada visualización parte de una <strong>pregunta de negocio</strong>, elimina el ruido visual y termina con una <strong>lectura objetiva</strong> — no es gráfico bonito por estética, es gráfico que decide.",
    },
    "analysis.story.01": {"pt": "Pergunta", "en": "Question", "es": "Pregunta"},
    "analysis.story.02": {"pt": "Visualização", "en": "Visualization", "es": "Visualización"},
    "analysis.story.03": {"pt": "Leitura", "en": "Reading", "es": "Lectura"},
    "analysis.story.04": {"pt": "Decisão", "en": "Decision", "es": "Decisión"},
    "analysis.tab.scatter": {"pt": "Dispersão", "en": "Scatter", "es": "Dispersión"},
    "analysis.tab.heatmap": {"pt": "Mapa de calor", "en": "Heatmap", "es": "Mapa de calor"},
    "analysis.tab.bars": {"pt": "Barras", "en": "Bars", "es": "Barras"},
    "analysis.tab.pie": {"pt": "Pizza", "en": "Pie", "es": "Pastel"},
    "analysis.tab.density": {"pt": "Densidade", "en": "Density", "es": "Densidad"},

    "analysis.q1.eyebrow": {"pt": "Pergunta 01", "en": "Question 01", "es": "Pregunta 01"},
    "analysis.q1.title": {"pt": "Quanto custa ser popular?", "en": "What does popularity cost?", "es": "¿Cuánto cuesta ser popular?"},
    "analysis.q1.sub": {"pt": "Será que produtos mais avaliados — os 'queridinhos' — também são os mais caros do catálogo?", "en": "Are the most-reviewed products — the 'darlings' — also the most expensive in the catalog?", "es": "¿Los productos más valorados — los 'consentidos' — son también los más caros del catálogo?"},
    "analysis.q1.chart.title": {"pt": "Preço × Popularidade", "en": "Price × Popularity", "es": "Precio × Popularidad"},
    "analysis.q1.chart.sub": {"pt": "Cada bolha é um produto. Eixo X: avaliações. Eixo Y: preço. Cor: nota. Tamanho: vendas.", "en": "Each bubble is a product. X-axis: reviews. Y-axis: price. Color: rating. Size: sales.", "es": "Cada burbuja es un producto. Eje X: reseñas. Eje Y: precio. Color: calificación. Tamaño: ventas."},

    "analysis.q2.eyebrow": {"pt": "Pergunta 02", "en": "Question 02", "es": "Pregunta 02"},
    "analysis.q2.title": {"pt": "Quais métricas andam juntas?", "en": "Which metrics move together?", "es": "¿Qué métricas se mueven juntas?"},
    "analysis.q2.sub": {"pt": "Saber o que se correlaciona é o primeiro passo para construir hipóteses de negócio defensáveis.", "en": "Knowing what correlates is the first step to building defensible business hypotheses.", "es": "Saber qué se correlaciona es el primer paso para construir hipótesis de negocio defendibles."},
    "analysis.q2.chart.title": {"pt": "Mapa de correlações entre métricas", "en": "Correlation heatmap between metrics", "es": "Mapa de correlaciones entre métricas"},
    "analysis.q2.chart.sub": {"pt": "Coeficiente de Pearson: laranja é correlação positiva, azul é negativa.", "en": "Pearson coefficient: orange is positive correlation, blue is negative.", "es": "Coeficiente de Pearson: naranja es correlación positiva, azul es negativa."},

    "analysis.q3.eyebrow": {"pt": "Pergunta 03", "en": "Question 03", "es": "Pregunta 03"},
    "analysis.q3.title": {"pt": "Quem domina a vitrine?", "en": "Who dominates the storefront?", "es": "¿Quién domina la vitrina?"},
    "analysis.q3.sub": {"pt": "Quanto da long tail é ocupada pelas marcas líderes e onde mora a oportunidade.", "en": "How much of the long tail is occupied by leading brands and where the opportunity lives.", "es": "Cuánto de la long tail ocupan las marcas líderes y dónde está la oportunidad."},
    "analysis.q3.chart.title": {"pt": "Top 10 marcas por volume de produtos", "en": "Top 10 brands by product volume", "es": "Top 10 marcas por volumen de productos"},
    "analysis.q3.chart.sub": {"pt": "Volume bruto no catálogo, ordenado.", "en": "Raw volume in the catalog, ordered.", "es": "Volumen bruto en el catálogo, ordenado."},

    "analysis.q4.eyebrow": {"pt": "Pergunta 04", "en": "Question 04", "es": "Pregunta 04"},
    "analysis.q4.title": {"pt": "Para quem é feita esta coleção?", "en": "Who is this collection made for?", "es": "¿Para quién es esta colección?"},
    "analysis.q4.sub": {"pt": "O equilíbrio entre os públicos é um sinal direto do posicionamento do marketplace.", "en": "Balance among audiences is a direct signal of marketplace positioning.", "es": "El equilibrio entre públicos es señal directa del posicionamiento del marketplace."},
    "analysis.q4.chart.title": {"pt": "Distribuição por gênero", "en": "Distribution by gender", "es": "Distribución por género"},
    "analysis.q4.chart.sub": {"pt": "Donut do catálogo completo.", "en": "Donut of the complete catalog.", "es": "Donut del catálogo completo."},

    "analysis.q5.eyebrow": {"pt": "Pergunta 05", "en": "Question 05", "es": "Pregunta 05"},
    "analysis.q5.title": {"pt": "Existe efeito de temporada no preço?", "en": "Is there a season effect on price?", "es": "¿Hay efecto de temporada en el precio?"},
    "analysis.q5.sub": {"pt": "Comparar a densidade revela se cada estação tem preço típico próprio ou se vivemos um catálogo atemporal.", "en": "Comparing density reveals whether each season has its own typical price or if we live in a timeless catalog.", "es": "Comparar la densidad revela si cada estación tiene un precio típico propio o si vivimos en un catálogo atemporal."},
    "analysis.q5.chart.title": {"pt": "Densidade de preço por temporada", "en": "Price density by season", "es": "Densidad de precio por temporada"},
    "analysis.q5.chart.sub": {"pt": "Onde o violino é largo, é onde os preços se concentram.", "en": "Where the violin is wide is where prices concentrate.", "es": "Donde el violín es ancho es donde se concentran los precios."},

    "analysis.read": {"pt": "Resposta", "en": "Answer", "es": "Respuesta"},

    # ===== ML =====
    "ml.lab.kicker": {"pt": "03 · LABORATÓRIO · STORYTELLING APLICADO", "en": "03 · LAB · APPLIED STORYTELLING", "es": "03 · LABORATORIO · STORYTELLING APLICADO"},
    "ml.lab.title": {
        "pt": "Do gráfico estático à <em>decisão</em> automatizada.",
        "en": "From static chart to automated <em>decision</em>.",
        "es": "Del gráfico estático a la <em>decisión</em> automatizada.",
    },
    "ml.lab.copy": {
        "pt": "Notebook de exploração responde <strong>o que aconteceu</strong>. Este laboratório responde <strong>o que provavelmente vai acontecer</strong> — e <strong>o que o cliente sente</strong>. Dois modelos lado a lado: um <strong>Random Forest regressor</strong> que estima ticket e expõe sua incerteza; um leitor lexical de reviews que traduz milhares de opiniões em duas listas acionáveis. Foi exatamente para fechar essa lacuna entre análise e ação que o projeto foi construído.",
        "en": "Exploration notebooks answer <strong>what happened</strong>. This lab answers <strong>what is likely to happen</strong> — and <strong>what customers feel</strong>. Two models side by side: a <strong>Random Forest regressor</strong> that estimates ticket and exposes its uncertainty; a lexical review reader that translates thousands of opinions into two actionable lists. The project was built precisely to close this gap between analysis and action.",
        "es": "Los notebooks de exploración responden <strong>qué pasó</strong>. Este laboratorio responde <strong>qué probablemente pase</strong> — y <strong>qué siente el cliente</strong>. Dos modelos lado a lado: un <strong>Random Forest regressor</strong> que estima ticket y expone su incertidumbre; un lector léxico de reseñas que traduce miles de opiniones en dos listas accionables. El proyecto se construyó precisamente para cerrar esa brecha entre análisis y acción.",
    },
    "ml.section1.eyebrow": {"pt": "Modelo 01 · Random Forest Regressor", "en": "Model 01 · Random Forest Regressor", "es": "Modelo 01 · Random Forest Regressor"},
    "ml.section1.title": {"pt": "Estimador de preço", "en": "Price estimator", "es": "Estimador de precio"},
    "ml.section1.subtitle": {
        "pt": "O modelo aprendeu padrões entre marca, material, temporada, gênero, nota e popularidade — e devolve a faixa provável para um produto qualquer.",
        "en": "The model learned patterns between brand, material, season, gender, rating, and popularity — and returns the likely range for any product.",
        "es": "El modelo aprendió patrones entre marca, material, temporada, género, calificación y popularidad — y devuelve el rango probable para cualquier producto.",
    },
    "ml.kpi.mae": {"pt": "MAE (erro médio)", "en": "MAE (mean error)", "es": "MAE (error medio)"},
    "ml.kpi.mae.trend": {"pt": "quanto menor, melhor", "en": "the lower, the better", "es": "cuanto menor, mejor"},
    "ml.kpi.r2": {"pt": "R² (qualidade)", "en": "R² (quality)", "es": "R² (calidad)"},
    "ml.kpi.r2.trend": {"pt": "máximo = 1.0", "en": "max = 1.0", "es": "máximo = 1.0"},
    "ml.kpi.train": {"pt": "Amostras de treino", "en": "Training samples", "es": "Muestras de entrenamiento"},
    "ml.kpi.train.trend": {"pt": "80% do dataset", "en": "80% of dataset", "es": "80% del dataset"},
    "ml.kpi.test": {"pt": "Amostras de teste", "en": "Test samples", "es": "Muestras de prueba"},
    "ml.kpi.test.trend": {"pt": "20% do dataset", "en": "20% of dataset", "es": "20% del dataset"},

    "ml.sim.eyebrow": {"pt": "Playground interativo", "en": "Interactive playground", "es": "Playground interactivo"},
    "ml.sim.title": {"pt": "Simulador de preço", "en": "Price simulator", "es": "Simulador de precio"},
    "ml.sim.subtitle": {
        "pt": "Configure um produto fictício à esquerda; o modelo devolve um preço estimado e a faixa de incerteza entre as 120 árvores.",
        "en": "Configure a fictional product on the left; the model returns an estimated price and the uncertainty range across the 120 trees.",
        "es": "Configura un producto ficticio a la izquierda; el modelo devuelve un precio estimado y el rango de incertidumbre entre los 120 árboles.",
    },
    "ml.form.eyebrow": {"pt": "ATRIBUTOS DO PRODUTO", "en": "PRODUCT ATTRIBUTES", "es": "ATRIBUTOS DEL PRODUCTO"},
    "ml.form.expected_rating": {"pt": "Nota esperada", "en": "Expected rating", "es": "Calificación esperada"},
    "ml.form.review_volume": {"pt": "Volume de avaliações", "en": "Review volume", "es": "Volumen de reseñas"},
    "ml.form.discount": {"pt": "Desconto aplicado (%)", "en": "Applied discount (%)", "es": "Descuento aplicado (%)"},
    "ml.form.submit": {"pt": "✦  Estimar preço", "en": "✦  Estimate price", "es": "✦  Estimar precio"},
    "ml.result.label": {"pt": "PREÇO ESTIMADO", "en": "ESTIMATED PRICE", "es": "PRECIO ESTIMADO"},
    "ml.result.range.tpl": {"pt": "faixa provável: R$ {0} – R$ {1}", "en": "likely range: R$ {0} – R$ {1}", "es": "rango probable: R$ {0} – R$ {1}"},
    "ml.result.position.above.tpl": {"pt": "acima da mediana do catálogo (R$ {0}) em {1}%", "en": "above catalog median (R$ {0}) by {1}%", "es": "por encima de la mediana del catálogo (R$ {0}) en {1}%"},
    "ml.result.position.below.tpl": {"pt": "abaixo da mediana do catálogo (R$ {0}) em {1}%", "en": "below catalog median (R$ {0}) by {1}%", "es": "por debajo de la mediana del catálogo (R$ {0}) en {1}%"},
    "ml.waiting.title": {"pt": "Pronto para inferir", "en": "Ready to infer", "es": "Listo para inferir"},
    "ml.waiting.body": {
        "pt": "Monte um perfil de produto à esquerda e clique em <strong>Estimar preço</strong>. A faixa devolvida espelha a dispersão entre as 120 árvores do Random Forest — quanto mais largo o intervalo, mais incerto o modelo está sobre aquele perfil.",
        "en": "Build a product profile on the left and click <strong>Estimate price</strong>. The returned range mirrors the dispersion across the 120 Random Forest trees — the wider the interval, the more uncertain the model is about that profile.",
        "es": "Arma un perfil de producto a la izquierda y haz clic en <strong>Estimar precio</strong>. El rango devuelto refleja la dispersión entre los 120 árboles del Random Forest — cuanto más amplio el intervalo, más incierto está el modelo sobre ese perfil.",
    },

    "ml.feat.eyebrow": {"pt": "Interpretabilidade", "en": "Interpretability", "es": "Interpretabilidad"},
    "ml.feat.title": {"pt": "Quais atributos pesam mais", "en": "Which attributes weigh most", "es": "Qué atributos pesan más"},
    "ml.feat.subtitle": {
        "pt": "Ranqueia o que o modelo aprendeu a olhar primeiro. Use como bússola para precificação e curadoria.",
        "en": "Ranks what the model learned to look at first. Use as a compass for pricing and curation.",
        "es": "Clasifica lo que el modelo aprendió a mirar primero. Úsalo como brújula para fijar precios y curaduría.",
    },
    "ml.feat.chart.title": {"pt": "Variáveis que mais explicam o preço", "en": "Variables that best explain price", "es": "Variables que más explican el precio"},
    "ml.feat.chart.sub": {"pt": "Importância pela redução média de impureza nas árvores.", "en": "Importance by mean impurity reduction across trees.", "es": "Importancia por reducción media de impureza en los árboles."},

    "ml.section2.eyebrow": {"pt": "Modelo 02 · NLP lexical", "en": "Model 02 · Lexical NLP", "es": "Modelo 02 · NLP léxico"},
    "ml.section2.title": {"pt": "A voz do cliente, em duas listas", "en": "Customer's voice, in two lists", "es": "La voz del cliente, en dos listas"},
    "ml.section2.subtitle": {
        "pt": "Reviews escritos pelos compradores, processados por correspondência exata em português — limpeza, lematização leve, contagem por palavra-chave.",
        "en": "Reviews written by buyers, processed by exact matching in Portuguese — cleaning, light lemmatization, keyword counting.",
        "es": "Reseñas escritas por compradores, procesadas por coincidencia exacta en portugués — limpieza, lematización ligera, conteo por palabra clave.",
    },
    "ml.kpi.reviews": {"pt": "Reviews válidos", "en": "Valid reviews", "es": "Reseñas válidas"},
    "ml.kpi.pos": {"pt": "Menções positivas", "en": "Positive mentions", "es": "Menciones positivas"},
    "ml.kpi.neg": {"pt": "Menções negativas", "en": "Negative mentions", "es": "Menciones negativas"},
    "ml.kpi.ratio": {"pt": "Razão pos / neg", "en": "Pos / neg ratio", "es": "Razón pos / neg"},
    "ml.kpi.ratio.trend": {"pt": "quanto maior, mais favorável", "en": "the higher, the more favorable", "es": "cuanto mayor, más favorable"},
    "ml.chart.pos.title": {"pt": "Top elogios", "en": "Top praises", "es": "Top elogios"},
    "ml.chart.pos.sub": {"pt": "Palavras mais celebradas pelos clientes.", "en": "Words most celebrated by customers.", "es": "Palabras más celebradas por los clientes."},
    "ml.chart.neg.title": {"pt": "Top reclamações", "en": "Top complaints", "es": "Top reclamos"},
    "ml.chart.neg.sub": {"pt": "Palavras mais frequentes em reviews negativos.", "en": "Most frequent words in negative reviews.", "es": "Palabras más frecuentes en reseñas negativas."},

    # ===== Sobre =====
    "about.hero.eyebrow": {"pt": "04 · Bastidores", "en": "04 · Behind the scenes", "es": "04 · Detrás de escena"},
    "about.hero.title": {"pt": "Sobre o <em>projeto</em>", "en": "About the <em>project</em>", "es": "Sobre el <em>proyecto</em>"},
    "about.hero.subtitle": {
        "pt": "Um experimento de portfólio que une visualização de dados, design editorial e machine learning em um único produto navegável.",
        "en": "A portfolio experiment combining data visualization, editorial design, and machine learning into a single navigable product.",
        "es": "Un experimento de portafolio que une visualización de datos, diseño editorial y machine learning en un único producto navegable.",
    },
    "about.motivation.eyebrow": {"pt": "Motivação", "en": "Motivation", "es": "Motivación"},
    "about.motivation.title": {"pt": "Por que esse projeto existe", "en": "Why this project exists", "es": "Por qué existe este proyecto"},
    "about.motivation.body": {
        "pt": "Este app nasceu como entrega do **Módulo 10 — Visualização de Dados** da formação Cientista de Dados, que pedia cinco gráficos clássicos sobre um dataset de e-commerce de moda. Em vez de parar no notebook, a entrega virou um produto: um dashboard multi-página, interativo, com identidade visual editorial e dois modelos de machine learning rodando em produção.\n\nO objetivo é mostrar, em uma única peça, três competências:\n\n- **Análise exploratória** — extrair leitura de negócio de dados brutos.\n- **Design de produto** — transformar gráficos em narrativa visual.\n- **Aplicação de IA** — entregar valor preditivo, não só descritivo.",
        "en": "This app was born as a deliverable for **Module 10 — Data Visualization** of the Data Scientist program, which required five classic charts on a fashion e-commerce dataset. Instead of stopping at the notebook, the deliverable became a product: a multi-page interactive dashboard with editorial visual identity and two machine learning models running in production.\n\nThe goal is to show, in a single piece, three competencies:\n\n- **Exploratory analysis** — extracting business readings from raw data.\n- **Product design** — turning charts into visual narrative.\n- **AI application** — delivering predictive value, not just descriptive.",
        "es": "Esta app nació como entrega del **Módulo 10 — Visualización de Datos** de la formación de Científico de Datos, que pedía cinco gráficos clásicos sobre un dataset de e-commerce de moda. En vez de quedarse en el notebook, la entrega se volvió un producto: un dashboard multipágina, interactivo, con identidad visual editorial y dos modelos de machine learning corriendo en producción.\n\nEl objetivo es mostrar, en una sola pieza, tres competencias:\n\n- **Análisis exploratorio** — extraer lectura de negocio de datos brutos.\n- **Diseño de producto** — transformar gráficos en narrativa visual.\n- **Aplicación de IA** — entregar valor predictivo, no solo descriptivo.",
    },
    "about.stack.eyebrow": {"pt": "STACK TECNOLÓGICA", "en": "TECH STACK", "es": "STACK TECNOLÓGICO"},
    "about.arch.eyebrow": {"pt": "Arquitetura", "en": "Architecture", "es": "Arquitectura"},
    "about.arch.title": {"pt": "Como o app está organizado", "en": "How the app is organized", "es": "Cómo está organizada la app"},
    "about.arch.subtitle": {"pt": "Separação clara entre dados, lógica visual e páginas — pronto para crescer.", "en": "Clear separation between data, visual logic, and pages — ready to grow.", "es": "Separación clara entre datos, lógica visual y páginas — listo para crecer."},
    "about.author.eyebrow": {"pt": "Autor", "en": "Author", "es": "Autor"},
    "about.author.title": {"pt": "Conectar", "en": "Connect", "es": "Conectar"},
    "about.author.subtitle": {"pt": "Cientista de dados em formação · entusiasta de produtos data-driven.", "en": "Data scientist in training · enthusiast of data-driven products.", "es": "Científico de datos en formación · entusiasta de productos data-driven."},
    "about.btn.portfolio": {"pt": "Meu portfólio", "en": "My portfolio", "es": "Mi portafolio"},

    # ===== Footer =====
    "footer.body": {
        "pt": "<strong>Moda em Dados</strong> — Projeto de portfólio por <a href=\"https://allefyrafael.codes/\" target=\"_blank\" rel=\"noopener\" class=\"footer-author\">Allefy Rafael</a> · Visualização e ML aplicados ao e-commerce de moda brasileiro.",
        "en": "<strong>Fashion in Data</strong> — Portfolio project by <a href=\"https://allefyrafael.codes/\" target=\"_blank\" rel=\"noopener\" class=\"footer-author\">Allefy Rafael</a> · Visualization and ML applied to Brazilian fashion e-commerce.",
        "es": "<strong>Moda en Datos</strong> — Proyecto de portafolio por <a href=\"https://allefyrafael.codes/\" target=\"_blank\" rel=\"noopener\" class=\"footer-author\">Allefy Rafael</a> · Visualización y ML aplicados al e-commerce de moda brasileño.",
    },

    # ===== Common =====
    "lang.label": {"pt": "Idioma", "en": "Language", "es": "Idioma"},
}


def get_lang() -> str:
    return st.session_state.get("lang", "pt")


def set_lang(lang: str) -> None:
    if lang in LANGUAGES:
        st.session_state["lang"] = lang


def t(key: str, *args) -> str:
    """Retorna a string traduzida para o idioma atual.
    Aceita argumentos posicionais para templates com {0}, {1}, etc."""
    lang = get_lang()
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    text = entry.get(lang) or entry.get("pt") or key
    if args:
        try:
            return text.format(*args)
        except (IndexError, KeyError):
            return text
    return text


def language_selector() -> None:
    """Seletor de idioma via st.button (soft rerun, sem reload de página).

    Usa session_state para persistir entre interações. As bandeiras são
    aplicadas via CSS ::before nas classes geradas pela key do botão.
    """
    if "lang" not in st.session_state:
        st.session_state["lang"] = "pt"
    current = st.session_state["lang"]

    st.markdown(
        '<div class="lang-bar-wrap">'
        f'<div class="lang-bar-label">{t("lang.label")}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns([7, 1, 1, 1])
    for i, code in enumerate(("pt", "en", "es")):
        with cols[i + 1]:
            cfg = LANGUAGES[code]
            is_active = code == current
            if st.button(
                cfg["code"],
                key=f"lang_{code}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=cfg["label"],
            ):
                set_lang(code)
                st.rerun()
