"""Model adapter registry.

Adapters are imported lazily: registering or creating an HTTP-backed adapter
must not drag in torch/transformers, which an API-only environment does not
have installed.
"""

from typing import Any, Dict

from brbbq.models.base import BaseModelAdapter


def _load(name: str):
    if name in ("huggingface_causal_lm", "bode_alpaca"):
        from brbbq.models.huggingface import BodeAlpacaAdapter, HuggingFaceCausalLMAdapter
        return {"huggingface_causal_lm": HuggingFaceCausalLMAdapter,
                "bode_alpaca": BodeAlpacaAdapter}[name]
    if name == "maritaca_api":
        from brbbq.models.maritaca import MaritacaAPIAdapter
        return MaritacaAPIAdapter
    if name == "openai_replay":
        from brbbq.models.openai_replay import OpenAIReplayAdapter
        return OpenAIReplayAdapter
    return None


ADAPTER_NAMES = ("huggingface_causal_lm", "bode_alpaca", "maritaca_api", "openai_replay")


def create_adapter(config: Dict[str, Any]) -> BaseModelAdapter:
    name = config.get("adapter", "huggingface_causal_lm")
    adapter = _load(name)
    if adapter is None:
        raise ValueError("Unknown model adapter: {}".format(name))
    return adapter(config)


def __getattr__(name: str):  # keep `from brbbq.models import BodeAlpacaAdapter` working
    for key in ADAPTER_NAMES:
        cls = None
        try:
            cls = _load(key)
        except ModuleNotFoundError:
            continue
        if cls is not None and cls.__name__ == name:
            return cls
    raise AttributeError(name)


__all__ = ["BaseModelAdapter", "create_adapter", "ADAPTER_NAMES"]
