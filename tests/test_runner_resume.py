import pandas as pd

from brbbq.models.base import BaseModelAdapter
from brbbq.scoring.runner import run_inference


class FakeAdapter(BaseModelAdapter):
    def __init__(self):
        super().__init__({"model_name": "fake", "adapter": "fake", "prompt_style": "simple"})
        self.calls = 0

    def load_tokenizer(self):
        return object()

    def load_model(self):
        return object()

    def render_prompt(self, example):
        return example["context"]

    def get_devices(self):
        return ["cpu"]

    def option_token_metadata(self):
        return {
            "letters": {
                letter: {
                    "considered_token_ids": [ord(letter)],
                    "variants": [],
                    "variant_count": 3,
                    "considered_id_count": 1,
                }
                for letter in "ABC"
            }
        }

    def score_options(self, prompts):
        self.calls += 1
        return [
            {
                "predicted_option": "A",
                "logprob_A": 0.0,
                "logprob_B": -1.0,
                "logprob_C": -2.0,
                "n_input_tokens": 4,
            }
            for _ in prompts
        ]

    def generate_free(self, prompt, max_new_tokens):
        return "A", 1

    def metadata(self):
        return {"adapter": "fake", "model_name": "fake", "devices": ["cpu"]}


def test_runner_checkpoint_deduplicates_and_resumes(tmp_path):
    rows = []
    for index in range(3):
        rows.append(
            {
                "example_id": "ex{}".format(index),
                "logical_id": "log{}".format(index),
                "language": "pt",
                "category_id": "regionality",
                "context_type": "ambiguous",
                "question_type": "negative",
                "context": "x",
                "question": "y",
                "correct_content": "unknown",
                "biased_content": "group1",
                "selected_content": "unknown",
                "content_of_A": "group1",
                "content_of_B": "group2",
                "content_of_C": "unknown",
                "correct_option": "C",
                "biased_option": "A",
                "unknown_position": "C",
                "permutation_index": index,
                "group1": "g1",
                "group2": "g2",
                "brazil_specific": True,
                "aggregation": "core",
                "bias_target_id": "g1",
                "scenario_id": "s",
                "needs_human_validation": True,
            }
        )
    expanded = pd.DataFrame(rows)
    run_dir = tmp_path / "run"
    (run_dir / "logs").mkdir(parents=True)
    (run_dir / "metrics").mkdir()
    (run_dir / "checkpoints").mkdir()
    (run_dir / "manifest.json").write_text('{"status":"initialized"}', encoding="utf-8")
    config = {
        "model": {"model_name": "fake"},
        "experiment": {"seed": 42},
        "inference": {
            "batch_size": 2,
            "checkpoint_every": 1,
            "audit_per_language": 0,
            "max_new_tokens_audit": 1,
        },
    }
    adapter = FakeAdapter()
    first = run_inference(config, run_dir, expanded, adapter=adapter)
    assert len(first) == 3 and first["example_id"].nunique() == 3
    calls = adapter.calls
    second = run_inference(config, run_dir, expanded, adapter=adapter)
    assert len(second) == 3 and adapter.calls == calls
