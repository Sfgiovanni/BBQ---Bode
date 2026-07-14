import pandas as pd

from brbbq.models.base import BaseModelAdapter
from brbbq.scoring.runner import run_inference
from brbbq.utils.io import atomic_json


class DeterministicAdapter(BaseModelAdapter):
    def load_tokenizer(self):
        return self

    def load_model(self):
        return self

    def render_prompt(self, example):
        return "{}|{}|{}".format(example["language"], example["context"], example["question"])

    def get_devices(self):
        return ["cpu"]

    def option_token_metadata(self):
        return {
            "letters": {
                letter: {"considered_token_ids": [index], "variant_count": 3}
                for index, letter in enumerate("ABC")
            }
        }

    def score_options(self, prompts):
        return [
            {
                "predicted_option": "A",
                "logprob_A": -0.1,
                "logprob_B": -1.0,
                "logprob_C": -2.0,
                "n_input_tokens": len(prompt),
            }
            for prompt in prompts
        ]

    def generate_free(self, prompt, max_new_tokens):
        return "A", 1

    def metadata(self):
        return {"model_name": self.config["model_name"], "devices": ["cpu"]}


def _config():
    return {
        "experiment": {"seed": 42},
        "model": {"model_name": "test/deterministic"},
        "inference": {"batch_size": 2, "checkpoint_every": 2, "audit_per_language": 0},
    }


def test_scoring_is_deterministic():
    adapter = DeterministicAdapter({"model_name": "test/deterministic"})
    assert adapter.score_options(["x", "y"]) == adapter.score_options(["x", "y"])
    assert adapter.get_devices() == ["cpu"]


def test_checkpoint_resume_has_no_duplicates(tmp_path, dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    subset = pd.concat(
        [
            expanded[expanded["language"] == "pt"].head(3),
            expanded[expanded["language"] == "en"].head(3),
        ],
        ignore_index=True,
    )
    run_dir = tmp_path / "run"
    for name in ("logs", "metrics", "checkpoints"):
        (run_dir / name).mkdir(parents=True, exist_ok=True)
    atomic_json({"status": "initialized"}, run_dir / "manifest.json")
    adapter = DeterministicAdapter({"model_name": "test/deterministic"})
    first = run_inference(_config(), run_dir, subset, adapter=adapter)
    second = run_inference(_config(), run_dir, subset, adapter=adapter)
    assert len(first) == len(second) == 6
    assert second["example_id"].is_unique


def test_gpu_contract_when_available():
    import torch

    if torch.cuda.is_available():
        assert torch.cuda.device_count() >= 1
