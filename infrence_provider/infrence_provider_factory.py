from typing import Any, Dict

from infrence_provider.groq_interface import GroqInterface
from infrence_provider.infrence_provider import InferenceProvider
from infrence_provider.ollama_interface import OllamaInterface


class InferenceProviderFactory:
    """
    Factory class to create instances of InferenceProvider based on configuration.
    """
    PROVIDER_MAP = {
        'groq': GroqInterface,
        'ollama': OllamaInterface,
    }

    @staticmethod
    def create_provider(config: Dict[str, Any]) -> InferenceProvider:
        """
        Creates an instance of an InferenceProvider based on the 'active_provider_type'
        key in the configuration dictionary.

        Args:
            config: A dictionary containing the configuration. Must include
                    'provider_type' (e.g., 'groq', 'ollama') and provider-specific
                    settings (e.g., 'groq_config', 'ollama_config').

        Returns:
            An instance of a class implementing InferenceProvider.

        Raises:
            ValueError: If 'active_provider_type' is missing or invalid, or if the
                        provider-specific config is missing/invalid.
        """
        provider_type = config.get('active_provider_type')
        if not provider_type:
            raise ValueError(
                "Configuration must include 'active_provider_type' (e.g., 'groq', 'ollama')")

        provider_class = InferenceProviderFactory.PROVIDER_MAP.get(
            provider_type.lower())
        if not provider_class:
            raise ValueError(f"Invalid provider_type: '{provider_type}'. "
                             f"Valid types are: {list(InferenceProviderFactory.PROVIDER_MAP.keys())}")

        # Get the specific configuration section for the chosen provider
        provider_config_key_name = f"{provider_type.lower()}_config"
        # Default to empty dict if key missing
        provider_config = config.get(provider_config_key_name, {})

        try:
            # Instantiate the chosen provider class with its specific configuration
            instance = provider_class(provider_config)
            return instance
        except Exception as e:
            raise ValueError(f"Error initializing {provider_type} provider "
                             f"from config '{provider_config_key_name}': {e}") from e
