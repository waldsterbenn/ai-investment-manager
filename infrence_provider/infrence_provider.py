import os
from abc import ABC, abstractmethod
from typing import Dict, Any


class InferenceProvider(ABC):
    """
    Abstract Base Class defining the interface for an inference provider.
    """
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        """Initialize the provider with specific configuration."""
        pass

    @abstractmethod
    def infer(self, prompt: str, temperature: float = 1.0) -> str:
        """
        Perform inference based on the given prompt.
        kwargs can be used for provider-specific parameters like temperature, max_tokens etc.
        """
        pass

    @abstractmethod
    def infer_structured(self, prompt: str, expected_format: str, temperature: float = 1.0) -> str:
        """
        Perform inference based on the given prompt.
        kwargs can be used for provider-specific parameters like temperature, max_tokens etc.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of the provider."""
        pass

    @abstractmethod
    def get_provider_llm(self) -> str:
        """Return the model name of the provider."""
        pass
