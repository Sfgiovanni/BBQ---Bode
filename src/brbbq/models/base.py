"""Abstract interface isolating model-specific behavior."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence, Tuple


class BaseModelAdapter(ABC):
    """Contract required by the inference runner."""

    def __init__(self, config: Dict[str, Any]):
        self.config = dict(config)

    @abstractmethod
    def load_tokenizer(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def load_model(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def render_prompt(self, example: Dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_devices(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def option_token_metadata(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def score_options(self, prompts: Sequence[str]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def generate_free(self, prompt: str, max_new_tokens: int) -> Tuple[str, int]:
        raise NotImplementedError

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        raise NotImplementedError
