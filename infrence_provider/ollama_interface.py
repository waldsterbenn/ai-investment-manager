
from typing import Any, Dict
import ollama
from infrence_provider.infrence_provider import InferenceProvider


class OllamaInterface(InferenceProvider):
    """
    Concrete implementation for the Ollama inference provider.
    """

    def __init__(self, config: Dict[str, Any]):
        self.base_url: str = config.get(
            'base_url', 'http://localhost:11434')  # Default URL
        self.model: str = config.get('model', 'llama3')  # Default model
        self.context_window: str = config.get(
            'context_window', '32000')  # Default context windoww

        print(
            f"Initializing OllamaInterface with base_url: {self.base_url}, model: {self.model}")
        self.client = ollama.Client(
            host=self.base_url
        )

    def infer(self, prompt: str, temperature: float = 1.0) -> str:

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": temperature,
                     "context_window": self.context_window},
            stream=False)

        return response['response']

    def infer_structured(self, prompt: str, expected_format: str, temperature: float = 1.0) -> str:
        raise NotImplementedError(
            "Structured inference is not implemented for OllamaInterface.")

    def get_provider_name(self) -> str:
        return "Ollama"

    def get_provider_llm(self) -> str:
        return self.model
