"""Hugging Face causal-language-model adapters."""

import os
import platform
from typing import Any, Dict, List, Sequence, Tuple

import torch

from brbbq.models.base import BaseModelAdapter
from brbbq.prompts import render_prompt
from brbbq.scoring.tokens import audit_letter_tokens


DTYPES = {
    "float16": torch.float16,
    "bfloat16": torch.bfloat16,
    "float32": torch.float32,
}


class HuggingFaceCausalLMAdapter(BaseModelAdapter):
    """Generic first-token scorer for Hugging Face causal LMs."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.tokenizer = None
        self.model = None
        self._token_metadata = None

    def load_tokenizer(self) -> Any:
        if self.tokenizer is not None:
            return self.tokenizer
        from transformers import AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.get("tokenizer_name") or self.config["model_name"],
            revision=self.config.get("tokenizer_revision"),
            token=os.environ.get("HF_TOKEN"),
            use_fast=False,
            trust_remote_code=bool(self.config.get("trust_remote_code", False)),
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        return self.tokenizer

    def load_model(self) -> Any:
        if self.model is not None:
            return self.model
        from transformers import AutoModelForCausalLM

        dtype_name = self.config.get("dtype", "float32")
        if dtype_name not in DTYPES:
            raise ValueError("Unsupported dtype: {}".format(dtype_name))
        self.load_tokenizer()
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config["model_name"],
            revision=self.config.get("revision"),
            token=os.environ.get("HF_TOKEN"),
            torch_dtype=DTYPES[dtype_name],
            device_map=self.config.get("device_map", "auto"),
            low_cpu_mem_usage=bool(self.config.get("low_cpu_mem_usage", True)),
            trust_remote_code=bool(self.config.get("trust_remote_code", False)),
        )
        self.model.eval()
        return self.model

    def render_prompt(self, example: Dict[str, Any]) -> str:
        return render_prompt(
            example, self.config.get("prompt_style", "simple"), self.load_tokenizer()
        )

    def _input_device(self) -> torch.device:
        model = self.load_model()
        if hasattr(model, "hf_device_map"):
            for key in ("model.embed_tokens", "transformer.wte", "model.decoder.embed_tokens"):
                location = model.hf_device_map.get(key)
                if location is not None and str(location) not in ("disk", "cpu"):
                    return torch.device(
                        "cuda:{}".format(location) if isinstance(location, int) else location
                    )
        for parameter in model.parameters():
            if parameter.device.type != "meta":
                return parameter.device
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def get_devices(self) -> List[str]:
        model = self.load_model()
        if hasattr(model, "hf_device_map"):
            return sorted({str(value) for value in model.hf_device_map.values()})
        return [str(self._input_device())]

    def option_token_metadata(self) -> Dict[str, Any]:
        if self._token_metadata is None:
            self._token_metadata = audit_letter_tokens(self.load_tokenizer())
        return self._token_metadata

    @torch.inference_mode()
    def score_options(self, prompts: Sequence[str]) -> List[Dict[str, Any]]:
        tokenizer, model = self.load_tokenizer(), self.load_model()
        encoded = tokenizer(list(prompts), return_tensors="pt", padding=True)
        device = self._input_device()
        encoded = {key: value.to(device) for key, value in encoded.items()}
        output = model(**encoded)
        logprobs = torch.log_softmax(output.logits[:, -1, :].float(), dim=-1)
        metadata = self.option_token_metadata()["letters"]
        rows = []
        for index in range(len(prompts)):
            scores = {}
            for letter in ("A", "B", "C"):
                ids = metadata[letter]["considered_token_ids"]
                scores[letter] = float(torch.logsumexp(logprobs[index, ids], dim=0).item())
            prediction = max(scores, key=scores.get)
            rows.append(
                {
                    "predicted_option": prediction,
                    "logprob_A": scores["A"],
                    "logprob_B": scores["B"],
                    "logprob_C": scores["C"],
                    "n_input_tokens": int(encoded["attention_mask"][index].sum().item()),
                }
            )
        return rows

    @torch.inference_mode()
    def generate_free(self, prompt: str, max_new_tokens: int) -> Tuple[str, int]:
        tokenizer, model = self.load_tokenizer(), self.load_model()
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self._input_device()) for key, value in inputs.items()}
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
        new_tokens = output[0][inputs["input_ids"].shape[-1] :]
        return tokenizer.decode(new_tokens, skip_special_tokens=True).strip(), len(new_tokens)

    def metadata(self) -> Dict[str, Any]:
        import transformers

        return {
            "adapter": self.config.get("adapter", "huggingface_causal_lm"),
            "model_name": self.config["model_name"],
            "model_revision": self.config.get("revision"),
            "tokenizer_name": self.config.get("tokenizer_name") or self.config["model_name"],
            "tokenizer_revision": self.config.get("tokenizer_revision"),
            "dtype": self.config.get("dtype"),
            "device_map": self.config.get("device_map"),
            "devices": self.get_devices(),
            "torch_version": torch.__version__,
            "transformers_version": transformers.__version__,
            "python_version": platform.python_version(),
            "cuda_available": torch.cuda.is_available(),
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        }


class BodeAlpacaAdapter(HuggingFaceCausalLMAdapter):
    """BODE specialization that enforces its Alpaca prompt contract."""

    def __init__(self, config: Dict[str, Any]):
        config = dict(config)
        config.setdefault("prompt_style", "alpaca")
        if config["prompt_style"] != "alpaca":
            raise ValueError("BodeAlpacaAdapter requires prompt_style=alpaca")
        super().__init__(config)
