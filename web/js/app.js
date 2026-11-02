// Moda em Dados — versão estática do app Streamlit (streamlit_app/).
// Cada página tem <body data-page="...">; os dados vêm de data/*.json gerados por tools/build_static.py.
(function () {
  "use strict";

  var COLORS = {
    primary: "#C2410C", ink: "#1F2937", muted: "#9CA3AF", gold: "#D4A574",
    line: "#E7E2D9", plum: "#7C3AED", moss: "#059669", petrol: "#0891B2",
  };
  var PALETTE = [COLORS.primary, COLORS.gold, COLORS.plum, COLORS.moss, COLORS.petrol, "#DC2626", "#0EA5E9", "#A16207"];
  var LANGS = ["pt", "en", "es"];
  var HTML_LANG = { pt: "pt-BR", en: "en", es: "es" };
  var LANG_KEY = "moda-lang";

  var page = document.body.getAttribute("data-page");
  var app = document.getElementById("app");
  var dict = null;
  var lang = "pt";
  var cache = {};

  // ---------- utilidades ----------
  function readLang() {
    var fromUrl = new URLSearchParams(location.search).get("lang");
    if (LANGS.indexOf(fromUrl) >= 0) return fromUrl;
    try {
      var saved = localStorage.getItem(LANG_KEY);
      if (LANGS.indexOf(saved) >= 0) return saved;
    } catch (e) { /* armazenamento indisponível */ }
    return "pt";
  }

  function t(key) {
    var text = (dict && dict[lang] && dict[lang][key]) || (dict && dict.pt[key]) || key;
    var args = Array.prototype.slice.call(arguments, 1);
    return text.replace(/\{(\d+)\}/g, function (m, i) { return args[i] !== undefined ? args[i] : m; });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function load(name) {
    if (!cache[name]) {
      cache[name] = fetch("data/" + name + ".json").then(function (r) {
        if (!r.ok) throw new Error(name + " " + r.status);
        return r.json();
      });
    }
    return cache[name];
  }

  // Formatos do app original: milhar com ponto (f"{n:,}".replace(",", ".")) e decimais com ponto.
  function fmtInt(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
  function fix(n, d) { return Number(n).toFixed(d); }
  function brl(v) {
    var parts = Number(v).toFixed(2).split(".");
    return "R$ " + parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "," + parts[1];
  }
  function mean(a) { return a.reduce(function (s, v) { return s + v; }, 0) / a.length; }
  function median(a) {
    var s = a.slice().sort(function (x, y) { return x - y; });
    var mid = Math.floor(s.length / 2);
    return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
  }
  function uniqSorted(a) {
    return Array.from(new Set(a)).sort(function (x, y) { return x < y ? -1 : x > y ? 1 : 0; });
  }
  function valueCounts(values) {
    var order = [], counts = {};
    values.forEach(function (v) {
      if (!(v in counts)) { counts[v] = 0; order.push(v); }
      counts[v]++;
    });
    return order.map(function (k) { return [k, counts[k]]; })
      .sort(function (a, b) { return b[1] - a[1]; });
  }

  // ---------- blocos visuais (equivalentes a utils/theme.py) ----------
  function hero(eyebrow, title, sub) {
    return '<div class="hero"><div class="hero-eyebrow">' + eyebrow + '</div><h1 class="hero-title">' +
      title + '</h1><p class="hero-sub">' + sub + "</p></div>";
  }
  function section(eyebrow, title, sub) {
    return '<div class="section-eyebrow">' + eyebrow + '</div><h2 class="section-title">' + title +
      '</h2><p class="section-sub">' + (sub || "") + "</p>";
  }
  function chartTitle(title, sub) {
    return '<div class="chart-head"><h3 class="chart-title">' + title + "</h3>" +
      (sub ? '<p class="chart-sub">' + sub + "</p>" : "") + "</div>";
  }
  function insight(text, label) {
    return '<div class="insight"><div class="insight-label">' + label + '</div><p class="insight-text">' + text + "</p></div>";
  }
  function kpi(label, value, unit, trend) {
    return "<div class='kpi-card'><div class='kpi-label'>" + label + "</div><div class='kpi-value'>" + value +
      (unit ? "<span class='unit'>" + unit + "</span>" : "") + "</div>" +
      (trend ? "<div class='kpi-trend'>" + trend + "</div>" : "") + "</div>";
  }
  function kpiGrid(cards) { return "<div class='kpi-grid'>" + cards.join("") + "</div>"; }

  // ---------- gráficos (equivalentes a utils/charts.py) ----------
  function baseLayout(height, extra) {
    var layout = {
      font: { family: "DM Sans, sans-serif", color: COLORS.ink, size: 13 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      margin: { l: 16, r: 24, t: 30, b: 48 },
      xaxis: { gridcolor: COLORS.line, zerolinecolor: COLORS.line, automargin: true },
      yaxis: { gridcolor: COLORS.line, zerolinecolor: COLORS.line, automargin: true },
      legend: { font: { size: 12 } },
      height: height,
      modebar: { orientation: "h", bgcolor: "rgba(250,247,242,0.0)", activecolor: COLORS.primary, color: COLORS.muted },
    };
    Object.keys(extra || {}).forEach(function (k) {
      if (k === "xaxis" || k === "yaxis") Object.assign(layout[k], extra[k]);
      else layout[k] = extra[k];
    });
    return layout;
  }
  function plot(id, data, layout) {
    var el = document.getElementById(id);
    if (!el || !window.Plotly) return;
    el.innerHTML = "";
    window.Plotly.react(el, data, layout, { displaylogo: false, responsive: true });
  }

  function barTopBrands(id, rows, n) {
    var top = valueCounts(rows.map(function (r) { return r.b; })).slice(0, n).reverse();
    var x = top.map(function (e) { return e[1]; });
    plot(id, [{
      type: "bar", orientation: "h", x: x, y: top.map(function (e) { return e[0]; }), text: x,
      textposition: "outside", cliponaxis: false,
      textfont: { family: "DM Sans, sans-serif", size: 12, color: COLORS.ink },
      marker: { color: x, colorscale: [[0, COLORS.gold], [1, COLORS.primary]], showscale: false },
      hovertemplate: "<b>%{y}</b><br>%{x} produtos<extra></extra>",
    }], baseLayout(520, { xaxis: { title: { text: "Produtos no catálogo" } }, yaxis: { title: { text: "" } } }));
  }

  function histRatings(id, rows) {
    var x = rows.map(function (r) { return r.r; });
    var m = mean(x);
    plot(id, [{
      type: "histogram", x: x, nbinsx: 20, marker: { color: COLORS.primary, line: { width: 1, color: "white" } },
      opacity: 0.85, hovertemplate: "Nota: %{x}<br>%{y} produtos<extra></extra>",
    }], baseLayout(380, {
      xaxis: { title: { text: "Nota" } }, yaxis: { title: { text: "Produtos" } },
      shapes: [{ type: "line", xref: "x", yref: "paper", x0: m, x1: m, y0: 0, y1: 1, line: { color: COLORS.plum, dash: "dash" } }],
      annotations: [{ x: m, y: 1, xref: "x", yref: "paper", text: "média " + fix(m, 2), showarrow: false,
        xanchor: "right", yanchor: "top", font: { color: COLORS.plum } }],
    }));
  }

  // ---------- páginas ----------
  var pages = {};

  pages.home = function () {
    return load("products").then(function (data) {
      var m = data.kpis;
      var card = function (href, key, variant) {
        return '<a href="' + href + '" class="nav-card-html ' + (variant || "") + '">' +
          '<div class="nav-card-eyebrow">' + t("home.card." + key + ".eyebrow") + "</div>" +
          '<div class="nav-card-title">' + t("home.card." + key + ".title") + "</div>" +
          '<div class="nav-card-body">' + t("home.card." + key + ".body") + "</div>" +
          '<div class="nav-card-cta"><span class="cta-text">' + t("home.card." + key + ".cta") +
          '</span><span class="cta-arrow">→</span></div></a>';
      };
      var stat = function (bg, color, svg, value, label) {
        return '<div class="dataset-stat"><div class="dataset-stat-icon" style="background:' + bg + "; color:" + color + ';">' +
          '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
          svg + '</svg></div><div class="dataset-stat-value">' + value + '</div><div class="dataset-stat-label">' + label + "</div></div>";
      };
      app.innerHTML =
        hero(t("home.hero.eyebrow"), t("home.hero.title"), t("home.hero.subtitle")) +
        kpiGrid([
          kpi(t("home.kpi.products"), fmtInt(m.total), "", t("home.kpi.products.trend")),
          kpi(t("home.kpi.brands"), String(m.marcas), "", t("home.kpi.brands.trend")),
          kpi(t("home.kpi.rating"), fix(m.nota_media, 2), "/5", t("home.kpi.rating.trend")),
          kpi(t("home.kpi.ticket"), "R$ " + fix(m.preco_medio, 0), "", t("home.kpi.ticket.trend.tpl", fix(m.preco_mediano, 0))),
        ]) +
        '<div class="manifesto"><div class="manifesto-eyebrow">' + t("home.manifesto.eyebrow") + '</div><p class="manifesto-lead">' +
        t("home.manifesto.lead") + '</p><p class="manifesto-body">' + t("home.manifesto.body") + "</p></div>" +
        section(t("home.acts.eyebrow"), t("home.acts.title"), t("home.acts.subtitle")) +
        "<div class='nav-grid-html'>" + card("visao-geral.html", "dashboard") + card("analise.html", "analysis") +
        card("ml.html", "ml", "is-ml") + "</div>" +
        section(t("home.dataset.eyebrow"), t("home.dataset.title"), t("home.dataset.subtitle")) +
        '<div class="dataset-panel">' +
        stat("rgba(194,65,12,0.12)", "var(--primary)", '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', fmtInt(m.avaliacoes_total), t("ml.kpi.reviews")) +
        stat("rgba(212,165,116,0.18)", "#A16207", '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>', "R$ " + fix(m.preco_medio, 2), t("home.kpi.ticket")) +
        stat("rgba(124,58,237,0.12)", "var(--plum)", '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>', fix(m.nota_media, 2) + "/5", t("home.kpi.rating")) +
        stat("rgba(8,145,178,0.12)", "var(--petrol)", '<path d="M20 6 9 17l-5-5"/>', String(m.marcas), t("home.kpi.brands")) +
        "</div>";
    });
  };

  // Estado dos filtros da Visão Geral (mantido ao trocar de idioma).
  var filterState = null;

  pages.overview = function () {
    return load("products").then(function (data) {
      var rows = data.rows;
      var genders = uniqSorted(rows.map(function (r) { return r.g; }));
      var seasons = uniqSorted(rows.map(function (r) { return r.s; }));
      var brands = uniqSorted(rows.map(function (r) { return r.b; }));
      var prices = rows.map(function (r) { return r.p; });
      var pMin = Math.floor(Math.min.apply(null, prices)), pMax = Math.ceil(Math.max.apply(null, prices));
      var fresh = function () {
        return { brands: [], genders: genders.slice(), seasons: seasons.slice(), pMin: pMin, pMax: pMax, rating: 0, sort: { key: "n", dir: -1 } };
      };
      if (!filterState) filterState = fresh();
      var st = filterState;

      var checks = function (name, options, selected) {
        return options.map(function (o) {
          return '<label><input type="checkbox" name="' + name + '" value="' + esc(o) + '"' +
            (selected.indexOf(o) >= 0 ? " checked" : "") + "> " + esc(o) + "</label>";
        }).join("");
      };

      app.innerHTML = '<div id="overview-root">' +
        hero(t("overview.hero.eyebrow"), t("overview.hero.title"), t("overview.hero.subtitle")) +
        '<div class="filters">' +
        '<details class="filter"><summary>' + t("filter.brand") + '</summary><div class="filter-panel">' +
        '<div class="panel-title">' + t("filter.brand.select") + '</div>' +
        '<input type="search" id="brand-search" placeholder="' + esc(t("filter.brand.placeholder")) + '" aria-label="' + esc(t("filter.brand.select")) + '">' +
        '<div class="options" id="brand-options">' + checks("brand", brands, st.brands) + "</div></div></details>" +
        '<details class="filter"><summary>' + t("filter.gender") + '</summary><div class="filter-panel"><div class="panel-title">' +
        t("filter.gender.select") + '</div><div class="options">' + checks("gender", genders, st.genders) + "</div></div></details>" +
        '<details class="filter"><summary>' + t("filter.season") + '</summary><div class="filter-panel"><div class="panel-title">' +
        t("filter.season.select") + '</div><div class="options">' + checks("season", seasons, st.seasons) + "</div></div></details>" +
        '<details class="filter"><summary>' + t("filter.price") + '</summary><div class="filter-panel"><div class="panel-title">' +
        t("filter.price.label") + '</div><div class="range-row">' +
        '<label>min <input type="range" id="p-min" min="' + pMin + '" max="' + pMax + '" step="1" value="' + st.pMin + '"><output id="p-min-out"></output></label>' +
        '<label>max <input type="range" id="p-max" min="' + pMin + '" max="' + pMax + '" step="1" value="' + st.pMax + '"><output id="p-max-out"></output></label>' +
        "</div></div></details>" +
        '<details class="filter"><summary>' + t("filter.rating") + '</summary><div class="filter-panel"><div class="range-row">' +
        '<label>' + t("filter.rating") + ' <input type="range" id="r-min" min="0" max="5" step="0.5" value="' + st.rating + '"><output id="r-min-out"></output></label>' +
        "</div></div></details>" +
        '<button type="button" class="btn" id="clear">' + t("filter.clear") + "</button></div>" +
        '<div id="filter-summary"></div><div id="overview-body"></div></div>';

      var root = document.getElementById("overview-root");
      var body = document.getElementById("overview-body");
      var summary = document.getElementById("filter-summary");

      function collect(name) {
        return Array.prototype.map.call(root.querySelectorAll('input[name="' + name + '"]:checked'), function (i) { return i.value; });
      }

      function update() {
        st.brands = collect("brand");
        st.genders = collect("gender");
        st.seasons = collect("season");
        var a = Number(document.getElementById("p-min").value), b = Number(document.getElementById("p-max").value);
        st.pMin = Math.min(a, b); st.pMax = Math.max(a, b);
        st.rating = Number(document.getElementById("r-min").value);
        document.getElementById("p-min-out").textContent = "R$ " + st.pMin;
        document.getElementById("p-max-out").textContent = "R$ " + st.pMax;
        document.getElementById("r-min-out").textContent = fix(st.rating, 1);

        var chips = [];
        if (st.brands.length) chips.push(st.brands.length + " " + t("filter.brand").toLowerCase());
        if (st.genders.length < genders.length) chips.push(st.genders.length + " " + t("filter.gender").toLowerCase());
        if (st.seasons.length < seasons.length) chips.push(st.seasons.length + " " + t("filter.season").toLowerCase());
        if (st.pMin !== pMin || st.pMax !== pMax) chips.push("R$ " + st.pMin + "–R$ " + st.pMax);
        if (st.rating > 0) chips.push("≥ " + fix(st.rating, 1) + "★");
        summary.innerHTML = chips.length
          ? "<div class='filter-summary'>" + t("filter.summary.active") + chips.map(function (c) { return "<span>" + esc(c) + "</span>"; }).join(" · ") + "</div>"
          : "<div class='filter-summary muted'>" + t("filter.summary.none") + "</div>";

        var filtered = rows.filter(function (r) {
          return st.genders.indexOf(r.g) >= 0 && st.seasons.indexOf(r.s) >= 0 &&
            r.p >= st.pMin && r.p <= st.pMax && r.r >= st.rating &&
            (!st.brands.length || st.brands.indexOf(r.b) >= 0);
        });
        renderOverview(filtered, rows.length, body);
      }

      root.addEventListener("change", function (e) {
        if (e.target.matches('input[type="checkbox"]')) update();
      });
      ["p-min", "p-max", "r-min"].forEach(function (id) {
        document.getElementById(id).addEventListener("input", update);
      });
      document.getElementById("brand-search").addEventListener("input", function (e) {
        var q = e.target.value.trim().toLowerCase();
        Array.prototype.forEach.call(document.querySelectorAll("#brand-options label"), function (l) {
          l.hidden = q && l.textContent.toLowerCase().indexOf(q) < 0;
        });
      });
      document.getElementById("clear").addEventListener("click", function () {
        filterState = fresh();
        render();
      });
      update();
    });
  };

  function renderOverview(filtered, total, body) {
    if (!filtered.length) {
      body.innerHTML = '<div class="notice" role="status">' + t("filter.empty") + "</div>";
      return;
    }
    var prices = filtered.map(function (r) { return r.p; });
    var brandsN = new Set(filtered.map(function (r) { return r.b; })).size;
    var top = valueCounts(filtered.map(function (r) { return r.b; }))[0];
    var topRatings = filtered.filter(function (r) { return r.b === top[0]; }).map(function (r) { return r.r; });
    body.innerHTML =
      kpiGrid([
        kpi(t("overview.kpi.slice"), fmtInt(filtered.length), "", t("overview.kpi.slice.trend.tpl", fix(filtered.length / total * 100, 1))),
        kpi(t("overview.kpi.brands"), String(brandsN)),
        kpi(t("home.kpi.rating"), fix(mean(filtered.map(function (r) { return r.r; })), 2), "/5"),
        kpi(t("home.kpi.ticket"), "R$ " + fix(mean(prices), 0), "", t("home.kpi.ticket.trend.tpl", fix(median(prices), 0))),
      ]) +
      section(t("overview.section.composition.eyebrow"), t("overview.section.composition.title"), t("overview.section.composition.subtitle")) +
      '<div class="cols-2"><div class="chart-card">' + chartTitle(t("overview.chart.brands.title"), t("overview.chart.brands.sub")) +
      '<div class="chart" id="ch-brands"></div></div><div class="chart-card">' + chartTitle(t("overview.chart.ratings.title"), t("overview.chart.ratings.sub")) +
      '<div class="chart" id="ch-ratings"></div></div></div>' +
      insight("<strong>" + esc(top[0]) + "</strong> — <strong>" + top[1] + "</strong> (" + fix(top[1] / filtered.length * 100, 1) + "%) · " +
        fix(mean(topRatings), 2) + "/5", t("analysis.read")) +
      section(t("overview.section.detail.eyebrow"), t("overview.section.detail.title"), t("overview.section.detail.subtitle")) +
      '<div class="table-wrap" id="table"></div>';
    barTopBrands("ch-brands", filtered, 10);
    histRatings("ch-ratings", filtered);
    renderTable(filtered);
  }

  function renderTable(filtered) {
    var st = filterState;
    // Top 50 por número de avaliações (sem avaliação vai para o fim), depois ordenação escolhida na tabela.
    var top = filtered.slice().sort(function (a, b) {
      return (b.n == null ? -1 : b.n) - (a.n == null ? -1 : a.n);
    }).slice(0, 50);
    var cols = [
      ["t", "table.col.product"], ["b", "table.col.brand"], ["g", "table.col.gender"], ["s", "table.col.season"],
      ["m", "table.col.material"], ["r", "table.col.rating"], ["n", "table.col.reviews"], ["p", "table.col.price"],
    ];
    var key = st.sort.key, dir = st.sort.dir;
    top.sort(function (a, b) {
      var x = a[key], y = b[key];
      if (x == null) x = typeof y === "string" ? "" : -1;
      if (y == null) y = typeof x === "string" ? "" : -1;
      return (x < y ? -1 : x > y ? 1 : 0) * dir;
    });
    var head = cols.map(function (c) {
      var active = c[0] === key;
      return '<th scope="col" aria-sort="' + (active ? (dir > 0 ? "ascending" : "descending") : "none") + '"><button type="button" data-sort="' +
        c[0] + '">' + t(c[1]) + (active ? (dir > 0 ? " ↑" : " ↓") : "") + "</button></th>";
    }).join("");
    var bodyRows = top.map(function (r) {
      return "<tr><td class='title'>" + esc(r.t) + "</td><td>" + esc(r.b) + "</td><td>" + esc(r.g) + "</td><td>" + esc(r.s) +
        "</td><td>" + esc(r.m) + "</td><td class='num'>" + fix(r.r, 1) + "</td><td class='num'>" + (r.n == null ? 0 : Math.trunc(r.n)) +
        "</td><td class='num'>" + brl(r.p) + "</td></tr>";
    }).join("");
    var wrap = document.getElementById("table");
    wrap.innerHTML = '<table class="data"><thead><tr>' + head + "</tr></thead><tbody>" + bodyRows + "</tbody></table>";
    wrap.querySelectorAll("th button").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-sort");
        st.sort = { key: k, dir: st.sort.key === k ? -st.sort.dir : (k === "t" || k === "b" || k === "g" || k === "s" || k === "m" ? 1 : -1) };
        renderTable(filtered);
      });
    });
  }

  var activeTab = 0;

  pages.analysis = function () {
    return load("analysis").then(function (a) {
      var ins = a.insights;
      var tabs = [
        ["scatter", "q1", "<strong>R$ " + fix(ins.q1.mean, 2) + "</strong> · " + (ins.q1.delta >= 0 ? "+" : "") + fix(ins.q1.delta, 1) + "%"],
        ["heatmap", "q2", "avaliações × vendidos = <strong>" + fix(ins.q2.qa, 2) + "</strong> · preço × nota = <strong>" + fix(ins.q2.pn, 2) + "</strong>"],
        ["bars", "q3", "<strong>" + esc(ins.q3.brand) + "</strong> · " + ins.q3.count + " (" + fix(ins.q3.pct, 1) + "%)"],
        ["pie", "q4", "<strong>" + esc(ins.q4.gender) + "</strong> · <strong>" + fix(ins.q4.pct, 1) + "%</strong>"],
        ["density", "q5", "<strong>" + esc(ins.q5.top) + "</strong> R$ " + fix(ins.q5.top_price, 2) + " · <strong>" + esc(ins.q5.bottom) + "</strong> R$ " + fix(ins.q5.bottom_price, 2)],
      ];
      app.innerHTML =
        hero(t("analysis.hero.eyebrow"), t("analysis.hero.title"), t("analysis.hero.subtitle")) +
        '<div class="story-flow"><div class="story-flow-eyebrow">METODOLOGIA · STORYTELLING WITH DATA</div><div class="story-flow-grid">' +
        [1, 2, 3, 4].map(function (i) {
          return '<div class="story-cell' + (i === 4 ? " is-final" : "") + '"><div class="story-num">0' + i + '</div><div class="story-name">' + t("analysis.story.0" + i) + "</div></div>";
        }).join('<div class="story-link"></div>') + "</div></div>" +
        '<div class="tabs" role="tablist">' + tabs.map(function (tb, i) {
          return '<button type="button" role="tab" id="tab-' + i + '" aria-controls="panel-' + i + '" aria-selected="' + (i === activeTab) +
            '" tabindex="' + (i === activeTab ? 0 : -1) + '">' + t("analysis.tab." + tb[0]) + "</button>";
        }).join("") + "</div>" +
        tabs.map(function (tb, i) {
          var q = tb[1];
          return '<section role="tabpanel" id="panel-' + i + '" aria-labelledby="tab-' + i + '"' + (i === activeTab ? "" : " hidden") + ">" +
            section(t("analysis." + q + ".eyebrow"), t("analysis." + q + ".title"), t("analysis." + q + ".sub")) +
            chartTitle(t("analysis." + q + ".chart.title"), t("analysis." + q + ".chart.sub")) +
            '<div class="chart" id="ch-' + q + '"></div>' + insight(tb[2], t("analysis.read")) + "</section>";
        }).join("");

      var drawn = {};
      var draw = function (i) {
        if (drawn[i]) { window.Plotly.Plots.resize(document.getElementById("ch-" + tabs[i][1])); return; }
        drawn[i] = true;
        analysisCharts[tabs[i][1]](a);
      };
      var select = function (i, focus) {
        activeTab = i;
        tabs.forEach(function (_, j) {
          var tab = document.getElementById("tab-" + j);
          tab.setAttribute("aria-selected", String(j === i));
          tab.tabIndex = j === i ? 0 : -1;
          document.getElementById("panel-" + j).hidden = j !== i;
        });
        if (focus) document.getElementById("tab-" + i).focus();
        draw(i);
      };
      tabs.forEach(function (_, i) {
        var tab = document.getElementById("tab-" + i);
        tab.addEventListener("click", function () { select(i); });
        tab.addEventListener("keydown", function (e) {
          if (e.key === "ArrowRight") select((i + 1) % tabs.length, true);
          if (e.key === "ArrowLeft") select((i + tabs.length - 1) % tabs.length, true);
        });
      });
      draw(activeTab);
    });
  };

  var analysisCharts = {
    q1: function (a) {
      var s = a.scatter;
      var maxSize = Math.max.apply(null, s.size);
      plot("ch-q1", [{
        type: "scatter", mode: "markers", x: s.x, y: s.y,
        customdata: s.brand.map(function (b, i) { return [b, s.gender[i], s.season[i], s.rating[i]]; }),
        marker: {
          color: s.rating, size: s.size, sizemode: "area", sizeref: 2 * maxSize / (20 * 20), sizemin: 0,
          colorscale: [[0, COLORS.muted], [0.5, COLORS.gold], [1, COLORS.primary]],
          colorbar: { title: { text: "Nota" }, thickness: 14, outlinewidth: 0 },
          line: { width: 0.4, color: "white" }, opacity: 0.78,
        },
        hovertemplate: "Marca=%{customdata[0]}<br>Gênero=%{customdata[1]}<br>Temporada=%{customdata[2]}<br>Nota=%{customdata[3]:.1f}<br>Preço (R$)=%{y:.2f}<br>Número de avaliações=%{x}<extra></extra>",
      }], baseLayout(520, { xaxis: { title: { text: "Número de avaliações" } }, yaxis: { title: { text: "Preço (R$)" } } }));
    },
    q2: function (a) {
      var labels = { "Nota": "Nota", "N_Avaliações": "Avaliações", "Desconto": "Desconto", "Preço": "Preço", "Qtd_Vendidos_Num": "Qtd. Vendidos" };
      var pretty = a.corr.cols.map(function (c) { return labels[c] || c; });
      plot("ch-q2", [{
        type: "heatmap", z: a.corr.z, x: pretty, y: pretty, zmin: -1, zmax: 1, text: a.corr.z, texttemplate: "%{text:.2f}",
        textfont: { family: "DM Sans, sans-serif", size: 13, color: COLORS.ink },
        colorscale: [[0, "#0891B2"], [0.5, "#FAF7F2"], [1, COLORS.primary]],
        colorbar: { title: { text: "Correlação" }, thickness: 14, outlinewidth: 0 },
      }], baseLayout(480, { xaxis: { side: "bottom" } }));
    },
    q3: function () {
      return load("products").then(function (d) { barTopBrands("ch-q3", d.rows, 10); });
    },
    q4: function (a) {
      var total = a.genders.values.reduce(function (s, v) { return s + v; }, 0);
      plot("ch-q4", [{
        type: "pie", labels: a.genders.labels, values: a.genders.values, hole: 0.55, sort: false,
        marker: { colors: PALETTE.slice(0, a.genders.labels.length), line: { color: "white", width: 3 } },
        textinfo: "label+percent", textfont: { family: "DM Sans, sans-serif", size: 13, color: COLORS.ink },
        hovertemplate: "<b>%{label}</b><br>%{value} produtos (%{percent})<extra></extra>",
      }], baseLayout(480, {
        showlegend: false,
        annotations: [{ text: "<b>" + total + "</b><br><span style='font-size:11px;color:#9CA3AF'>PRODUTOS</span>", x: 0.5, y: 0.5,
          xref: "paper", yref: "paper", font: { size: 22, color: COLORS.ink }, showarrow: false }],
      }));
    },
    q5: function (a) {
      plot("ch-q5", a.violins.map(function (v, i) {
        return {
          type: "violin", y: v.y, name: v.name, box: { visible: true }, meanline: { visible: true },
          fillcolor: PALETTE[i % PALETTE.length], line: { color: COLORS.ink }, opacity: 0.75, points: false,
        };
      }), baseLayout(500, { yaxis: { title: { text: "Preço (R$)" } }, xaxis: { title: { text: "" } }, violinmode: "group", showlegend: false }));
    },
  };

  var mlForm = null;

  pages.ml = function () {
    return Promise.all([load("model"), load("reviews")]).then(function (res) {
      var model = res[0], rv = res[1], mt = model.metrics;
      var brands = Object.keys(model.marca_map).sort();
      var materials = Object.keys(model.material_map).sort();
      var seasons = Object.keys(model.temporada_map).sort();
      var genders = model.gen_columns.map(function (g) { return g.replace("Gen_", ""); });
      if (!mlForm) {
        mlForm = { brand: brands.indexOf("lupo") >= 0 ? "lupo" : brands[0], material: materials[0], season: seasons[0],
          gender: genders[0], rating: 4.5, reviews: 200, discount: 10, result: null };
      }
      var f = mlForm;
      var options = function (list, sel) {
        return list.map(function (o) { return '<option value="' + esc(o) + '"' + (o === sel ? " selected" : "") + ">" + esc(o) + "</option>"; }).join("");
      };
      var posTotal = Object.values(rv.pos).reduce(function (s, v) { return s + v; }, 0);
      var negTotal = Object.values(rv.neg).reduce(function (s, v) { return s + v; }, 0);

      app.innerHTML =
        '<div class="ml-lab-band"><div class="ml-lab-band-inner"><div class="ml-lab-kicker">' + t("ml.lab.kicker") +
        '</div><h1 class="ml-lab-title">' + t("ml.lab.title") + '</h1><p class="ml-lab-copy">' + t("ml.lab.copy") + "</p></div></div>" +
        section(t("ml.section1.eyebrow"), t("ml.section1.title"), t("ml.section1.subtitle")) +
        kpiGrid([
          kpi(t("ml.kpi.mae"), "R$ " + fix(mt.mae, 2), "", t("ml.kpi.mae.trend")),
          kpi(t("ml.kpi.r2"), fix(mt.r2, 3), "", t("ml.kpi.r2.trend")),
          kpi(t("ml.kpi.train"), fmtInt(mt.n_train), "", t("ml.kpi.train.trend")),
          kpi(t("ml.kpi.test"), fmtInt(mt.n_test), "", t("ml.kpi.test.trend")),
        ]) +
        section(t("ml.sim.eyebrow"), t("ml.sim.title"), t("ml.sim.subtitle")) +
        '<div class="cols-2"><form class="ml-form" id="ml-form"><div class="ml-form-eyebrow">' + t("ml.form.eyebrow") + '</div><div class="form-grid">' +
        '<label class="field">' + t("filter.brand") + '<select name="brand">' + options(brands, f.brand) + "</select></label>" +
        '<label class="field">' + t("filter.gender") + '<select name="gender">' + options(genders, f.gender) + "</select></label>" +
        '<label class="field">' + t("table.col.material") + '<select name="material">' + options(materials, f.material) + "</select></label>" +
        '<label class="field">' + t("ml.form.expected_rating") + ' <output id="o-rating"></output><input type="range" name="rating" min="1" max="5" step="0.1" value="' + f.rating + '"></label>' +
        '<label class="field">' + t("filter.season") + '<select name="season">' + options(seasons, f.season) + "</select></label>" +
        '<label class="field">' + t("ml.form.review_volume") + ' <output id="o-reviews"></output><input type="range" name="reviews" min="0" max="5000" step="50" value="' + f.reviews + '"></label>' +
        '<label class="field full">' + t("ml.form.discount") + ' <output id="o-discount"></output><input type="range" name="discount" min="0" max="90" step="5" value="' + f.discount + '"></label>' +
        '</div><button type="submit" class="btn btn-primary">' + t("ml.form.submit") + "</button></form>" +
        '<div id="ml-result" aria-live="polite"></div></div>' +
        section(t("ml.feat.eyebrow"), t("ml.feat.title"), t("ml.feat.subtitle")) +
        chartTitle(t("ml.feat.chart.title"), t("ml.feat.chart.sub")) + '<div class="chart" id="ch-feat"></div><div id="feat-insight"></div>' +
        section(t("ml.section2.eyebrow"), t("ml.section2.title"), t("ml.section2.subtitle")) +
        kpiGrid([
          kpi(t("ml.kpi.reviews"), fmtInt(rv.total_reviews)),
          kpi(t("ml.kpi.pos"), fmtInt(posTotal)),
          kpi(t("ml.kpi.neg"), fmtInt(negTotal)),
          kpi(t("ml.kpi.ratio"), fix(posTotal / Math.max(negTotal, 1), 1) + "×", "", t("ml.kpi.ratio.trend")),
        ]) +
        '<div class="cols-2 cols-even"><div class="chart-card">' + chartTitle(t("ml.chart.pos.title"), t("ml.chart.pos.sub")) +
        '<div class="chart" id="ch-pos"></div></div><div class="chart-card">' + chartTitle(t("ml.chart.neg.title"), t("ml.chart.neg.sub")) +
        '<div class="chart" id="ch-neg"></div></div></div><div id="rv-insight"></div>';

      var form = document.getElementById("ml-form");
      var outputs = function () {
        document.getElementById("o-rating").textContent = fix(form.rating.value, 1);
        document.getElementById("o-reviews").textContent = form.reviews.value;
        document.getElementById("o-discount").textContent = form.discount.value;
      };
      var showResult = function () {
        var box = document.getElementById("ml-result");
        if (!f.result) {
          box.innerHTML = '<div class="ml-waiting-card"><div class="ml-waiting-icon">✦</div><div class="ml-waiting-title">' + t("ml.waiting.title") +
            '</div><div class="ml-waiting-body">' + t("ml.waiting.body") + "</div></div>";
          return;
        }
        var r = f.result, med = model.preco_median, delta = (r.price / med - 1) * 100;
        var pos = t(delta >= 0 ? "ml.result.position.above.tpl" : "ml.result.position.below.tpl", fix(med, 0), fix(Math.abs(delta), 1));
        box.innerHTML = '<div class="price-result"><div class="label">' + t("ml.result.label") + '</div><div class="value">R$ ' + fix(r.price, 0) +
          '</div><div class="range">' + t("ml.result.range.tpl", fix(r.p10, 0), fix(r.p90, 0)) + '</div><div class="position">' + pos + "</div></div>";
      };
      form.addEventListener("input", function () {
        f.brand = form.brand.value; f.gender = form.gender.value; f.material = form.material.value; f.season = form.season.value;
        f.rating = Number(form.rating.value); f.reviews = Number(form.reviews.value); f.discount = Number(form.discount.value);
        outputs();
      });
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        f.result = window.ModaForest.predict(model, f);
        showResult();
      });
      outputs();
      showResult();

      // Importância agregada (gênero somado), como em pages/3_Insights_ML.py
      var labels = { "Marca_Cod": t("filter.brand"), "Material_Cod": t("table.col.material"), "Temporada_Cod": t("filter.season"),
        "Nota": t("home.kpi.rating"), "N_Avaliações": t("table.col.reviews"), "Desconto": t("ml.form.discount") };
      var agg = [], gen = 0;
      model.features.forEach(function (name, i) {
        if (name.indexOf("Gen_") === 0) gen += model.importances[i];
        else agg.push([labels[name] || name, model.importances[i]]);
      });
      agg.push([t("filter.gender"), gen]);
      agg.sort(function (a, b) { return b[1] - a[1]; });
      agg = agg.slice(0, 8);
      var asc = agg.slice().reverse();
      var imp = asc.map(function (e) { return e[1]; });
      plot("ch-feat", [{
        type: "bar", orientation: "h", x: imp, y: asc.map(function (e) { return e[0]; }), text: imp.map(function (v) { return fix(v, 3); }),
        textposition: "outside", cliponaxis: false,
        marker: { color: imp, colorscale: [[0, COLORS.gold], [1, COLORS.primary]], showscale: false },
      }], baseLayout(440, { xaxis: { title: { text: "Importância relativa" } }, yaxis: { title: { text: "" } } }));
      document.getElementById("feat-insight").innerHTML =
        insight("<strong>" + agg[0][0] + "</strong> · <strong>" + fix(agg[0][1] * 100, 1) + "%</strong>", t("ml.feat.eyebrow"));

      var reviewBars = function (id, counts, color) {
        var items = Object.keys(counts).map(function (k) { return [k, counts[k]]; })
          .sort(function (a, b) { return b[1] - a[1]; }).slice(0, 10).reverse();
        var x = items.map(function (e) { return e[1]; });
        plot(id, [{
          type: "bar", orientation: "h", x: x, y: items.map(function (e) { return e[0]; }), text: x, textposition: "outside", cliponaxis: false,
          marker: { color: color, line: { width: 0 } }, hovertemplate: "<b>%{y}</b><br>%{x} menções<extra></extra>",
        }], baseLayout(420, { xaxis: { title: { text: "Menções nos reviews" } }, yaxis: { title: { text: "" } }, showlegend: false }));
      };
      reviewBars("ch-pos", rv.pos, COLORS.moss);
      reviewBars("ch-neg", rv.neg, COLORS.primary);
      var topOf = function (counts) {
        return Object.keys(counts).reduce(function (best, k) { return best === null || counts[k] > counts[best] ? k : best; }, null);
      };
      var tp = topOf(rv.pos), tn = topOf(rv.neg);
      if (tp && tn) {
        document.getElementById("rv-insight").innerHTML = insight("<strong>“" + tp + "”</strong> · " + rv.pos[tp] + " · <strong>“" + tn + "”</strong> · " +
          rv.neg[tn], t("ml.section2.title"));
      }
    });
  };

  pages.about = function () {
    var stack = ["Plotly.js", "Pandas + NumPy", "Scikit-learn", "HTML + CSS + JavaScript", "Azure Static Web Apps"];
    app.innerHTML =
      hero(t("about.hero.eyebrow"), t("about.hero.title"), t("about.hero.subtitle")) +
      '<div class="cols-2"><div class="about-body">' + section(t("about.motivation.eyebrow"), t("about.motivation.title")) +
      t("about.motivation.body") + '</div><div class="stack-card"><div class="eyebrow">' + t("about.stack.eyebrow") + "</div><ul>" +
      stack.map(function (s) { return "<li><strong>" + s + "</strong></li>"; }).join("") + "</ul></div></div>" +
      section(t("about.arch.eyebrow"), t("about.arch.title"), t("about.arch.subtitle")) +
      '<pre class="tree">' + esc([
        "web/                         # site publicado (Azure Static Web Apps)",
        "├── index.html               # Home",
        "├── visao-geral.html         # Dashboard com filtros",
        "├── analise.html             # 5 gráficos",
        "├── ml.html                  # Random Forest + NLP no navegador",
        "├── sobre.html",
        "├── js/app.js · js/forest.js",
        "├── css/ · vendor/plotly",
        "└── data/*.json              # gerados por tools/build_static.py",
        "streamlit_app/               # versão Streamlit original (PT/EN/ES)",
        "tools/build_static.py        # dados, textos e modelo → JSON",
        "tools/check_model_parity.py  # navegador × scikit-learn",
      ].join("\n")) + "</pre>" +
      section(t("about.author.eyebrow"), t("about.author.title"), t("about.author.subtitle")) +
      '<div class="author-card"><h2><a class="author-name-link" href="https://allefyrafael.codes" target="_blank" rel="noopener noreferrer">Allefy Rafael</a></h2>' +
      '<p class="author-tagline">' + t("about.author.subtitle") + '</p><div class="author-actions">' +
      '<a class="btn-portfolio" href="https://allefyrafael.codes" target="_blank" rel="noopener noreferrer">' + t("about.btn.portfolio") + " →</a>" +
      '<a class="btn-ghost" href="https://github.com/allefyrafael" target="_blank" rel="noopener noreferrer">GitHub →</a>' +
      '<a class="btn-ghost" href="https://www.linkedin.com/in/allefyrafael" target="_blank" rel="noopener noreferrer">LinkedIn →</a></div></div>';
    return Promise.resolve();
  };

  // ---------- moldura comum ----------
  function renderChrome() {
    document.documentElement.lang = HTML_LANG[lang];
    document.querySelectorAll("[data-i18n]").forEach(function (el) { el.textContent = t(el.getAttribute("data-i18n")); });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) { el.innerHTML = t(el.getAttribute("data-i18n-html")); });
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      if (a.getAttribute("data-nav") === page) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
    document.querySelectorAll("[data-lang]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });
    var navTitle = { home: "nav.home", overview: "nav.overview", analysis: "nav.analysis", ml: "nav.ml", about: "nav.about" }[page];
    document.title = t(navTitle) + " — " + t("home.hero.title").replace(/<[^>]+>/g, "");
    document.getElementById("footer").innerHTML = t("footer.body");
  }

  function render() {
    renderChrome();
    return pages[page]().catch(function (err) {
      app.innerHTML = '<div class="notice" role="alert">Não foi possível carregar os dados (' + esc(err.message) + "). Recarregue a página.</div>";
    });
  }

  // Fecha os painéis de filtro ao clicar fora deles.
  document.addEventListener("click", function (e) {
    Array.prototype.forEach.call(app.querySelectorAll("details.filter[open]"), function (d) {
      if (!d.contains(e.target)) d.removeAttribute("open");
    });
  });

  document.querySelectorAll("[data-lang]").forEach(function (b) {
    b.addEventListener("click", function () {
      lang = b.getAttribute("data-lang");
      try { localStorage.setItem(LANG_KEY, lang); } catch (e) { /* armazenamento indisponível */ }
      render();
    });
  });

  lang = readLang();
  load("i18n").then(function (d) { dict = d; render(); }).catch(function (err) {
    app.innerHTML = '<div class="notice" role="alert">Não foi possível carregar o site (' + esc(err.message) + ").</div>";
  });
})();
