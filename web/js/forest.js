// Avaliação do Random Forest exportado por tools/build_static.py.
// O scikit-learn compara as entradas em float32 (X <= limiar → esquerda); Math.fround reproduz isso.
(function (root) {
  function predictTree(tree, x) {
    var feature = tree[0], threshold = tree[1], left = tree[2], right = tree[3], value = tree[4];
    var node = 0;
    while (feature[node] >= 0) { // folhas têm feature -2 (TREE_UNDEFINED do scikit-learn)
      node = Math.fround(x[feature[node]]) <= threshold[node] ? left[node] : right[node];
    }
    return value[node];
  }

  // Percentil com interpolação linear, igual ao padrão do numpy.percentile.
  function percentile(sorted, p) {
    var pos = (sorted.length - 1) * p / 100;
    var lo = Math.floor(pos), hi = Math.ceil(pos);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
  }

  function buildVector(model, input) {
    var x = model.features.map(function () { return 0; });
    var idx = function (name) { return model.features.indexOf(name); };
    x[idx("Marca_Cod")] = model.marca_map[input.brand] || 0;
    x[idx("Material_Cod")] = model.material_map[input.material] || 0;
    x[idx("Temporada_Cod")] = model.temporada_map[input.season] || 0;
    x[idx("Nota")] = input.rating;
    x[idx("N_Avaliações")] = input.reviews;
    x[idx("Desconto")] = input.discount;
    var gen = idx("Gen_" + input.gender);
    if (gen >= 0) x[gen] = 1;
    return x;
  }

  function predict(model, input) {
    var x = buildVector(model, input);
    var preds = model.trees.map(function (tree) { return predictTree(tree, x); });
    var mean = preds.reduce(function (a, b) { return a + b; }, 0) / preds.length;
    var sorted = preds.slice().sort(function (a, b) { return a - b; });
    return { price: mean, p10: percentile(sorted, 10), p90: percentile(sorted, 90) };
  }

  var api = { predict: predict, buildVector: buildVector, predictTree: predictTree, percentile: percentile };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ModaForest = api;
})(this);
