"""Compara a previsão do navegador (web/js/forest.js, via Node) com o scikit-learn.

Treina o mesmo modelo de tools/build_static.py, monta casos (todas as combinações de
marca × gênero com valores variados e um sorteio amplo dos demais campos) e exige
diferença < 0,01 R$ no preço e nos percentis 10/90.

Uso: python tools/check_model_parity.py   (requer Node.js, pandas, numpy e scikit-learn)
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_static as bs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOL = 0.01

NODE_RUNNER = """
const fs = require('fs');
const forest = require(process.argv[2]);
const model = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const cases = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
process.stdout.write(JSON.stringify(cases.map(c => forest.predict(model, c))));
"""


def main() -> None:
    df = bs.load_data()
    _, ctx = bs.build_model(df)
    model = ctx["model"]
    model_json = json.loads((ROOT / "web" / "data" / "model.json").read_text(encoding="utf-8"))
    features = model_json["features"]

    rng = np.random.default_rng(7)
    brands = sorted(model_json["marca_map"])
    materials = sorted(model_json["material_map"])
    seasons = sorted(model_json["temporada_map"])
    genders = [g.replace("Gen_", "") for g in model_json["gen_columns"]]

    cases = []
    for b in brands:
        for g in genders:
            cases.append({
                "brand": b, "gender": g,
                "material": materials[int(rng.integers(len(materials)))],
                "season": seasons[int(rng.integers(len(seasons)))],
                "rating": round(float(rng.uniform(1, 5)), 1),
                "reviews": int(rng.integers(0, 101)) * 50,
                "discount": float(int(rng.integers(0, 19)) * 5),
            })

    rows = []
    for c in cases:
        x = {
            "Marca_Cod": model_json["marca_map"].get(c["brand"], 0),
            "Material_Cod": model_json["material_map"].get(c["material"], 0),
            "Temporada_Cod": model_json["temporada_map"].get(c["season"], 0),
            "Nota": c["rating"], "N_Avaliações": c["reviews"], "Desconto": c["discount"],
        }
        for g in model_json["gen_columns"]:
            x[g] = 1 if g == f"Gen_{c['gender']}" else 0
        rows.append(x)
    X = pd.DataFrame(rows)[features].values
    # Mesma conta do app (média e percentis das árvores), vetorizada sobre todos os casos.
    per_tree = np.stack([tr.predict(X) for tr in model.estimators_], axis=1)
    p10, p90 = np.percentile(per_tree, [10, 90], axis=1)
    expected = list(zip(per_tree.mean(axis=1), p10, p90))

    with tempfile.TemporaryDirectory() as tmp:
        runner = Path(tmp) / "run.js"
        runner.write_text(NODE_RUNNER, encoding="utf-8")
        cases_path = Path(tmp) / "cases.json"
        cases_path.write_text(json.dumps(cases, ensure_ascii=False), encoding="utf-8")
        out = subprocess.run(
            ["node", str(runner), str(ROOT / "web" / "js" / "forest.js"),
             str(ROOT / "web" / "data" / "model.json"), str(cases_path)],
            capture_output=True, text=True, encoding="utf-8", check=True,
        ).stdout
    got = json.loads(out)

    worst = 0.0
    for e, g in zip(expected, got):
        worst = max(worst, abs(e[0] - g["price"]), abs(e[1] - g["p10"]), abs(e[2] - g["p90"]))
    print(f"casos: {len(cases)}  maior diferença: R$ {worst:.6f}")
    if worst >= TOL:
        sys.exit(1)


if __name__ == "__main__":
    main()
