#!/usr/bin/env python3
"""Score the BR-BBQ catalog with an OpenAI model through the Batch API.

Three phases, each a separate invocation so nothing is spent by accident:

    python3 scripts/openai_batch.py --prepare   # render prompts, price it (free)
    python3 scripts/openai_batch.py --submit    # upload and start the batches
    python3 scripts/openai_batch.py --collect   # wait, download, parse

`--collect` writes `work_openai/<model>/scores.json`, keyed by SHA-1 of the
rendered prompt, in the exact shape `brbbq.models.openai_replay` replays into
the normal runner. The runner then produces a `raw_predictions.parquet` with the
same schema as the BODE and Sabiá runs.

The key is read from OPENAI_API_KEY and never written to disk.
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from brbbq.config import load_config, project_path            # noqa: E402
from brbbq.dataset import build_dataset                        # noqa: E402
from brbbq.models.openai_replay import prompt_key              # noqa: E402
from brbbq.prompts import render_prompt                        # noqa: E402

LETTERS = ("A", "B", "C")
NEG_INF = float("-inf")

# Per-model, from the config: gpt-4o answers in exactly 1 token, which is what
# the BODE and Sabia runs also scored. gpt-5.4 emits 4 and 400s below that, so
# it needs headroom -- a difference worth carrying in config rather than in a
# constant that silently inflates the output bill for whichever model runs.
DEFAULT_MAX_COMPLETION_TOKENS = 1
# The binding limit is NOT the 50k requests/file -- it is the org's *enqueued
# token* ceiling, and it is per model and per usage tier: 900k for gpt-5.4 but
# only 90k for gpt-4o on this account. Sized from the config so a model with a
# different ceiling does not need a code change; batches go out one at a time
# because the ceiling covers everything queued simultaneously.
DEFAULT_REQS_PER_BATCH = 698


def _logsumexp(values):
    finite = [v for v in values if v != NEG_INF]
    if not finite:
        return NEG_INF
    top = max(finite)
    return top + math.log(sum(math.exp(v - top) for v in finite))


def _client():
    from openai import OpenAI

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("set OPENAI_API_KEY in the environment")
    return OpenAI(api_key=key)


def _rows(config):
    paths = config["paths"]
    _, _, expanded = build_dataset(
        project_path(paths["categories"]), project_path(paths["scenarios"])
    )
    style = config["model"].get("prompt_style", "simple")
    for row in expanded.to_dict("records"):
        yield row, render_prompt(row, style, None)


def _workdir(model):
    d = REPO / "work_openai" / model
    d.mkdir(parents=True, exist_ok=True)
    return d


def prepare(config, model, top_logprobs, max_out=DEFAULT_MAX_COMPLETION_TOKENS,
            per_batch=DEFAULT_REQS_PER_BATCH):
    work = _workdir(model)
    seen, files, block, part = set(), [], [], 0

    def flush():
        nonlocal block, part
        if not block:
            return
        path = work / "input_{:03d}.jsonl".format(part)
        path.write_text("".join(block), encoding="utf-8")
        files.append(path)
        block, part = [], part + 1

    n_dup = 0
    for row, prompt in _rows(config):
        key = prompt_key(prompt)
        if key in seen:          # identical prompts across rotations are scored once
            n_dup += 1
            continue
        seen.add(key)
        block.append(json.dumps({
            "custom_id": key,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_completion_tokens": max_out,
                "temperature": 0.0,
                "logprobs": True,
                "top_logprobs": top_logprobs,
            },
        }, ensure_ascii=False) + "\n")
        if len(block) >= per_batch:
            flush()
    flush()

    chars = sum(len(json.loads(l)["body"]["messages"][0]["content"])
                for f in files for l in f.read_text(encoding="utf-8").splitlines())
    n = len(seen)
    print("{} prompts unicos ({} duplicados nao reenviados), {} lote(s)".format(n, n_dup, len(files)))
    print("   {} chars de prompt".format(chars))
    print("   arquivos: {}".format(", ".join(f.name for f in files)))
    return files, n


def submit(config, model, top_logprobs):
    work = _workdir(model)
    manifest_path = work / "manifest.json"
    if manifest_path.exists():
        print("manifesto ja existe -- nao reenvio. Apague {} para refazer.".format(manifest_path))
        return json.loads(manifest_path.read_text())
    files, _ = prepare(config, model, top_logprobs)
    cli = _client()
    manifest = {"model": model, "batches": []}
    for path in files:
        up = cli.files.create(file=open(path, "rb"), purpose="batch")
        batch = cli.batches.create(
            input_file_id=up.id, endpoint="/v1/chat/completions",
            completion_window="24h", metadata={"description": "brbbq-{}".format(model)},
        )
        manifest["batches"].append({"file": path.name, "file_id": up.id, "batch_id": batch.id})
        print("   {} -> {} ({})".format(path.name, batch.id, batch.status))
    manifest_path.write_text(json.dumps(manifest, indent=1))
    return manifest


TERMINAL = {"completed", "failed", "expired", "cancelled"}


def collect(config, model, wait=True, interval=120):
    work = _workdir(model)
    manifest = json.loads((work / "manifest.json").read_text())
    cli = _client()

    while True:
        states, done, total, failed = [], 0, 0, 0
        for entry in manifest["batches"]:
            b = cli.batches.retrieve(entry["batch_id"])
            counts = b.request_counts
            states.append(b.status)
            done += counts.completed or 0
            total += counts.total or 0
            failed += counts.failed or 0
        print("{}  {}  {}/{} concluidas, {} falhas".format(
            time.strftime("%H:%M:%S"), dict((s, states.count(s)) for s in set(states)),
            done, total, failed), flush=True)
        if all(s in TERMINAL for s in states) or not wait:
            break
        time.sleep(interval)

    scores, bad, no_letter = {}, 0, 0
    for entry in manifest["batches"]:
        b = cli.batches.retrieve(entry["batch_id"])
        if b.status != "completed":
            print("   {} em '{}' -- pulando".format(b.id, b.status))
            continue
        raw = work / "output_{}.jsonl".format(b.id)
        if not raw.exists():
            raw.write_bytes(cli.files.content(b.output_file_id).read())
        if getattr(b, "error_file_id", None):
            err = work / "errors_{}.jsonl".format(b.id)
            err.write_bytes(cli.files.content(b.error_file_id).read())
            print("   erros gravados em {}".format(err))
        for line in raw.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            body = ((rec.get("response") or {}).get("body")) or {}
            try:
                choice = body["choices"][0]
                content = choice["logprobs"]["content"]
                usage = body.get("usage", {})
            except (KeyError, IndexError, TypeError):
                bad += 1
                continue
            buckets = {L: [] for L in LETTERS}
            variants = {L: [] for L in LETTERS}
            for cand in content[0]["top_logprobs"]:
                letter = cand["token"].strip()
                if letter in buckets:
                    buckets[letter].append(cand["logprob"])
                    variants[letter].append(cand["token"])
            vals = {L: (_logsumexp(buckets[L]) if buckets[L] else NEG_INF) for L in LETTERS}
            found = [L for L in LETTERS if vals[L] != NEG_INF]
            if not found:
                no_letter += 1
            scores[rec["custom_id"]] = {
                "predicted_option": max(LETTERS, key=lambda L: vals[L]) if found else None,
                "logprob_A": vals["A"], "logprob_B": vals["B"], "logprob_C": vals["C"],
                "n_input_tokens": int(usage.get("prompt_tokens") or 0),
                "letters_found": len(found),
                "letters_missing": ",".join(L for L in LETTERS if vals[L] == NEG_INF),
                "top_token": content[0]["token"],
            }
    out = work / "scores.json"
    out.write_text(json.dumps(scores), encoding="utf-8")
    print("\n{} resultados -> {}".format(len(scores), out))
    if bad:
        print("   {} respostas sem logprobs utilizaveis".format(bad))
    if no_letter:
        print("   {} respostas sem NENHUMA letra no top-k (predicao nula)".format(no_letter))
    return out


def _submit_one(cli, path, model):
    """Upload + create; returns the batch object (status is 'validating')."""
    up = cli.files.create(file=open(path, "rb"), purpose="batch")
    return cli.batches.create(
        input_file_id=up.id, endpoint="/v1/chat/completions",
        completion_window="24h", metadata={"description": "brbbq-{}".format(model)})


def _is_queue_full(batch):
    erros = getattr(batch, "errors", None)
    codes = [getattr(x, "code", None) for x in (getattr(erros, "data", None) or [])]
    return "token_limit_exceeded" in codes


def run_sequential(config, model, top_logprobs, max_out, per_batch, interval=30, pausa=25):
    """Submit one chunk at a time, waiting for each before queueing the next.

    Two things make this fiddlier than it looks, both learned the hard way:

    * The enqueued-token ceiling is per model and per tier (90k for gpt-4o here),
      so chunks must be small and strictly sequential.
    * `batches.create` always returns 'validating'. A queue-full rejection only
      surfaces when validation finishes, seconds later -- so it cannot be caught
      at submit time, and a retry loop wrapped around `create` never fires. The
      retry has to live around the whole submit-and-wait cycle, which is what
      this does.
    """
    work = _workdir(model)
    files, _ = prepare(config, model, top_logprobs, max_out, per_batch)
    state_path = work / "manifest.json"
    manifest = json.loads(state_path.read_text()) if state_path.exists() else {"model": model, "batches": []}
    manifest["batches"] = [b for b in manifest["batches"] if b.get("status") == "completed"]
    feitos = {b["file"] for b in manifest["batches"]}
    cli = _client()

    for path in files:
        if path.name in feitos:
            continue
        for tentativa in range(1, 13):
            batch = _submit_one(cli, path, model)
            while True:
                b = cli.batches.retrieve(batch.id)
                if b.status in TERMINAL:
                    break
                time.sleep(interval)
            c = b.request_counts
            if b.status == "completed":
                manifest["batches"].append(
                    {"file": path.name, "batch_id": b.id, "status": "completed"})
                state_path.write_text(json.dumps(manifest, indent=1))
                print("{} -> completed ({}/{}, {} falhas)".format(
                    path.name, c.completed, c.total, c.failed), flush=True)
                break
            if _is_queue_full(b):
                espera = min(60 * tentativa, 300)
                print("   {} rejeitado (fila cheia); nova tentativa em {}s".format(
                    path.name, espera), flush=True)
                time.sleep(espera)
                continue
            for x in (getattr(getattr(b, "errors", None), "data", None) or [])[:2]:
                print("   ERRO {}: {}".format(getattr(x, "code", None), getattr(x, "message", None)))
            raise SystemExit("lote {} terminou em '{}' -- parando".format(path.name, b.status))
        else:
            raise SystemExit("nao consegui enfileirar {} apos 12 tentativas".format(path.name))
        time.sleep(pausa)   # deixa a fila drenar antes do proximo
    print("todos os lotes concluidos")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/bilingual_openai_extended.yaml")
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--submit", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--no-wait", action="store_true")
    args = ap.parse_args()

    config = load_config(args.config)
    model = config["model"]["model_name"]
    top_logprobs = int(config["model"].get("top_logprobs", 5))
    max_out = int(config["model"].get("max_completion_tokens",
                                      DEFAULT_MAX_COMPLETION_TOKENS))
    per_batch = int(config["model"].get("reqs_per_batch", DEFAULT_REQS_PER_BATCH))

    if args.prepare:
        prepare(config, model, top_logprobs, max_out, per_batch)
    if args.submit:
        submit(config, model, top_logprobs)
    if args.run:
        run_sequential(config, model, top_logprobs, max_out, per_batch)
    if args.collect:
        collect(config, model, wait=not args.no_wait)


if __name__ == "__main__":
    main()
