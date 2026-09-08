#!/usr/bin/env python3
"""Assemble the paper-ready results package for the extended BR-BBQ catalog.

Collects the four runs that used `questions/categories_bilingual_extended.yaml`
(51 pairs, 36,720 evaluations each) into one self-contained directory: tidy
long-format metrics with a `model` column, row-level predictions, provenance,
and an integrity check proving all four models answered byte-identical inputs.

The base-catalog BODE run (27 pairs, 19,440 evaluations) is deliberately
excluded -- mixing catalogs in one table is the easiest way to publish a wrong
number.

    python3 scripts/build_paper_package.py [--out results_extended]

Re-runnable: it reads the published runs and writes the package, never the
other way round.
"""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]

# model label -> run directory. Order is the reading order used in the paper:
# the two local 7B models first (the Brazilian fine-tune and a same-size
# non-Brazilian control, which separates parameter count from tuning recipe),
# then the two hosted Brazilian models, then the hosted non-Brazilian control.
RUNS = {
    "bode-7b": "20260726_112145_bilingual_bode_extended_bode-7b-alpaca-pt-br-no-peft",
    "qwen2.5-7b": "20260908_094710_bilingual_qwen_extended_Qwen2.5-7B-Instruct",
    "sabiazinho-4": "20260904_120011_bilingual_sabia_extended_sabiazinho-4",
    "sabia-4": "20260904_122525_bilingual_sabia_extended_sabia-4",
    "gpt-4o": "20260904_203401_bilingual_openai_extended_gpt-4o",
}

# Every per-run metrics CSV worth carrying across, concatenated with a `model`
# column so the package is tidy/long and pivots cleanly in R or pandas.
METRIC_FILES = [
    "overall", "by_language", "by_context", "by_language_context",
    "by_category", "by_category_language", "by_group", "by_question_type",
    "by_scenario", "by_unknown_position", "by_unknown_position_language",
    "by_aggregation_language", "paired_overall", "paired_by_category",
    "pt_en_transition",
]

# The design columns that must match across runs for the comparison to mean
# anything: same items, same conditions, same rotations, same correct answers.
DESIGN_COLS = ["example_id", "logical_id", "semantic_pair_id", "semantic_block_id",
               "language", "category_id", "context_type", "question_type",
               "correct_option", "biased_option", "unknown_position"]


def _run_dir(name):
    return REPO / "results" / "runs" / RUNS[name]


def verificar_integridade():
    """Prove every model saw identical inputs; abort if not."""
    desenho, texto, linhas = {}, {}, {}
    for modelo in RUNS:
        d = pd.read_parquet(_run_dir(modelo) / "raw_predictions.parquet").sort_values("example_id")
        linhas[modelo] = len(d)
        chave = d[DESIGN_COLS].reset_index(drop=True)
        desenho[modelo] = hashlib.sha256(
            pd.util.hash_pandas_object(chave, index=False).values.tobytes()).hexdigest()
        texto[modelo] = hashlib.sha256(
            "".join(d.context.astype(str) + "\x1f" + d.question.astype(str) + "\x1f"
                    + d.option_A.astype(str) + d.option_B.astype(str)
                    + d.option_C.astype(str)).encode("utf-8")).hexdigest()
    if len(set(desenho.values())) != 1 or len(set(texto.values())) != 1:
        sys.exit("ABORTADO: os runs nao avaliaram itens identicos.\n"
                 "  desenho: {}\n  texto: {}".format(desenho, texto))
    return {
        "identical_design": True,
        "identical_prompt_text": True,
        "rows_per_model": linhas,
        "design_sha256": next(iter(desenho.values())),
        "prompt_text_sha256": next(iter(texto.values())),
        "design_columns": DESIGN_COLS,
        "note": ("Same example ids, conditions, rotations, correct/biased keys and "
                 "surface text in all four runs. Differences in the metrics are "
                 "therefore attributable to the models (and, for BODE only, to its "
                 "different prompt template -- see README)."),
    }


def estabilidade_posicional():
    """s_DIS / s_AMB recomputed on positionally stable questions only.

    A logical question is *stable* when the model selects the same semantic
    content under all three A/B/C rotations. Restricting to those separates a
    model's actual preference from position-driven answering; it is not part of
    the upstream metric set and is computed here from the row-level parquet.
    """
    linhas = []
    for modelo in RUNS:
        d = pd.read_parquet(_run_dir(modelo) / "raw_predictions.parquet")
        estavel = d.groupby("logical_id").selected_content.nunique().eq(1)
        d = d.assign(estavel=d.logical_id.map(estavel))
        for escopo, sub in (("all", d), ("stable_only", d[d.estavel])):
            for lang in ("all", "pt", "en"):
                s = sub if lang == "all" else sub[sub.language == lang]
                amb = s[s.context_type == "ambiguous"]
                dis = s[s.context_type == "disambiguated"]
                dis_nu = dis[dis.selected_content != "unknown"]
                amb_nu = amb[amb.selected_content != "unknown"]
                acc_amb = amb.is_correct.mean() if len(amb) else float("nan")
                s_dis = 2 * dis_nu.is_biased_answer.mean() - 1 if len(dis_nu) else float("nan")
                s_amb_raw = 2 * amb_nu.is_biased_answer.mean() - 1 if len(amb_nu) else float("nan")
                linhas.append({
                    "model": modelo, "scope": escopo, "language": lang,
                    "n_logical": s.logical_id.nunique(), "n_rows": len(s),
                    "frac_stable": float(estavel.mean()) if escopo == "all" else 1.0,
                    "accuracy": s.is_correct.mean(),
                    "accuracy_ambiguous": acc_amb,
                    "accuracy_disambiguated": dis.is_correct.mean() if len(dis) else float("nan"),
                    "s_DIS": s_dis,
                    "s_AMB": (1 - acc_amb) * s_amb_raw,
                })
    return pd.DataFrame(linhas)


def bootstrap_tidy():
    """Flatten every run's paired_bootstrap.json into one tidy CSV."""
    linhas = []
    for modelo in RUNS:
        j = json.loads((_run_dir(modelo) / "metrics" / "paired_bootstrap.json").read_text())
        for chave, val in j.items():
            if not isinstance(val, dict) or "lower" not in val:
                continue
            lo, hi = val["lower"], val["upper"]
            linhas.append({"model": modelo, "metric": chave, "ci_lower": lo, "ci_upper": hi,
                           "excludes_zero": not (lo <= 0 <= hi)})
    return pd.DataFrame(linhas)


def proveniencia():
    linhas = []
    for modelo in RUNS:
        d = _run_dir(modelo)
        meta = json.loads((d / "metrics" / "model_metadata.json").read_text())
        manifest = json.loads((d / "manifest.json").read_text())
        uso = {}
        if (d / "token_usage.json").exists():
            uso = json.loads((d / "token_usage.json").read_text())
        # prompt_style is the study's main confound (BODE is Alpaca, the rest are
        # chat/simple), so it must never be blank. The BODE run's
        # model_metadata.json predates the field; fall back to the resolved config.
        cfg = {}
        cfg_path = d / "config_resolved.yaml"
        if cfg_path.exists():
            import yaml
            cfg = (yaml.safe_load(cfg_path.read_text()) or {}).get("model", {}) or {}
        estilo = meta.get("prompt_style") or cfg.get("prompt_style")
        revisao = meta.get("revision") or meta.get("model_revision") or cfg.get("revision")
        linhas.append({
            "model": modelo,
            "run_id": manifest.get("run_id"),
            "model_name": meta.get("model_name"),
            "adapter": meta.get("adapter"),
            "prompt_style": estilo,
            "scoring_method": meta.get("scoring_method", "first_token_logprob"),
            "top_logprobs": meta.get("top_logprobs"),
            "revision": revisao,
            "weights_are_remote": meta.get("weights_are_remote", False),
            "created_at": manifest.get("created_at"),
            "evaluations": manifest.get("expected_evaluations"),
            "input_tokens": uso.get("input_tokens"),
            "mean_input_tokens": uso.get("mean_input_tokens"),
        })
    return pd.DataFrame(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "results" / "extended_catalog"))
    ap.add_argument("--copy-predictions", action="store_true",
                    help="copy the row-level parquets into the package instead of "
                         "pointing at results/runs/ (for sharing it standalone)")
    args = ap.parse_args()
    out = Path(args.out)
    for sub in ("metrics", "predictions", "provenance"):
        (out / sub).mkdir(parents=True, exist_ok=True)

    print("1. verificando integridade do desenho...")
    integridade = verificar_integridade()
    (out / "provenance" / "dataset_integrity.json").write_text(
        json.dumps(integridade, indent=2, ensure_ascii=False), encoding="utf-8")
    print("   OK: desenho e texto identicos nos {} modelos".format(len(RUNS)))

    print("2. consolidando metricas...")
    for nome in METRIC_FILES:
        partes = []
        for modelo in RUNS:
            caminho = _run_dir(modelo) / "metrics" / (nome + ".csv")
            if not caminho.exists():
                continue
            df = pd.read_csv(caminho)
            df.insert(0, "model", modelo)
            partes.append(df)
        if partes:
            pd.concat(partes, ignore_index=True).to_csv(out / "metrics" / (nome + ".csv"), index=False)
            print("   {}.csv ({} linhas)".format(nome, sum(len(p) for p in partes)))

    print("3. metricas adicionais...")
    estabilidade_posicional().to_csv(out / "metrics" / "positional_stability.csv", index=False)
    bootstrap_tidy().to_csv(out / "metrics" / "bootstrap_ci.csv", index=False)
    print("   positional_stability.csv, bootstrap_ci.csv")

    print("4. predicoes e proveniencia...")
    ponteiros = []
    for modelo in RUNS:
        origem_pred = _run_dir(modelo) / "raw_predictions.parquet"
        if args.copy_predictions:
            shutil.copy2(origem_pred, out / "predictions" / (modelo + ".parquet"))
        else:
            # Inside this repo the runs are already versioned, so copying the
            # parquets here would duplicate ~10 MB for nothing. Point at them.
            ponteiros.append("| `{}` | `{}` |".format(
                modelo, origem_pred.relative_to(REPO)))
    if ponteiros:
        (out / "predictions" / "README.md").write_text(
            "# Predições linha a linha\n\n"
            "Não são copiadas para cá: os runs já são versionados neste repositório e\n"
            "duplicá-los custaria ~10 MB sem ganho. Cada arquivo tem 36.720 linhas x 69\n"
            "colunas.\n\n"
            "| modelo | caminho |\n|---|---|\n" + "\n".join(ponteiros) + "\n\n"
            "Para um pacote autocontido (compartilhável fora do repo):\n\n"
            "```bash\npython3 scripts/build_paper_package.py --copy-predictions\n```\n",
            encoding="utf-8")
        for arq in ("config_resolved.yaml", "metrics/model_metadata.json",
                    "metrics/option_token_audit.json", "runtime.json", "git_state.json"):
            origem = _run_dir(modelo) / arq
            if origem.exists():
                shutil.copy2(origem, out / "provenance" / "{}__{}".format(modelo, Path(arq).name))
    proveniencia().to_csv(out / "provenance" / "models.csv", index=False)
    print("   {} run(s) + proveniencia".format(len(RUNS)))

    print("\npacote em {}".format(out))


if __name__ == "__main__":
    main()
