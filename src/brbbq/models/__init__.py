"""Model adapter registry."""

from typing import Any, Dict

from brbbq.models.base import BaseModelAdapter
from brbbq.models.huggingface import BodeAlpacaAdapter, HuggingFaceCausalLMAdapter


ADAPTERS = {
    "huggingface_causal_lm": HuggingFaceCausalLMAdapter,
    "bode_alpaca": BodeAlpacaAdapter,
}


def create_adapter(config: Dict[str, Any]) -> BaseModelAdapter:
    name = config.get("adapter", "huggingface_causal_lm")
    if name not in ADAPTERS:
        raise ValueError("Unknown model adapter: {}".format(name))
    return ADAPTERS[name](config)


__all__ = ["BaseModelAdapter", "HuggingFaceCausalLMAdapter", "BodeAlpacaAdapter", "create_adapter"]
