import json
import logging
import logging.config
from typing import Any, Dict, Optional
from groq import Groq
import os

from infrence_provider.infrence_provider import InferenceProvider

config_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../config/'))

# Load the logging configuration
logging.config.fileConfig(os.path.join(config_path, "logging.config"))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


class GroqInterface(InferenceProvider):
    """
    Concrete implementation for the Groq inference provider.
    """

    def __init__(self, config: Dict[str, Any]):

        # Fetching the api key is a bit tricky, as it is not present in the config file.
        # It is passed in the api_keys.json file, which is another file in the config folder.
        # This is done to avoid hardcoding the api key in the config file.
        # The api_keys.json file is not present in the repository, so it is assumed that the user will create it.
        try:
            with open(os.path.join(config_path, "api_keys.json")) as keysFile:
                api_keys = json.load(keysFile)
        except FileNotFoundError as e:
            log.error(e)

        # Get groq key from api_keys.json
        api_key = api_keys[config.get('name_of_api_key')]
        self.api_key: Optional[str] = api_key or os.environ.get('GROQ_API_KEY')
        self.model: str = config.get('model', 'llama3-8b-8192')

        if not self.api_key:
            raise ValueError(
                "Groq API key is required. Provide it in config or set GROQ_API_KEY env var.")

        print(f"Initializing GroqInterface with model: {self.model}")
        # initialize the Groq client
        self.client = Groq(api_key=self.api_key)

    def infer(self, prompt: str, temperature: float = 1.0) -> str:
        # Placeholder for actual Groq API call
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=temperature,
            # max_completion_tokens=1024,
            # top_p=1,
        )
        return response.choices[0].message.content or ""

    def infer_structured(self, prompt: str, expected_format: str, temperature: float = 1.0) -> str:
        # Placeholder for actual Groq API call
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}, {
                "role": "assistant",
                "content": f"```{expected_format}"
            }],
            model=self.model,
            temperature=temperature,
            # max_completion_tokens=1024,
            # top_p=1,
            stop="```",
        )
        return response.choices[0].message.content or ""

    def get_provider_name(self) -> str:
        return "Groq"

    def get_provider_llm(self) -> str:
        return self.model
