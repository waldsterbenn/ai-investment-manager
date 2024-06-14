from enum import Enum


class LlmModelConfig:
    def __init__(self, name, context_window):
        self.name = name
        self.context_window = context_window


class SupportedModels(Enum):
    mistral_7B_v1 = 1
    mistral_7B_v2 = 2
    dolphin_2_8_mistral_v02 = 3
    hermes_2_pro_mistral = 4
    gemma_1_1_it = 5
    mixtral_8x_7b = 6
    wizardLm2_7b = 7
    llama3_8b = 8
    llama3_70b = 9
    llama3_gradient = 10
    phi3_medium = 11
    qwen2_7b = 12
    llama3_8b_q8 = 13


# Før man kan bruge andre modeller skal man hente dem via "ollama pull <modelname>"
llm_models_config = {
    SupportedModels.mistral_7B_v1:  LlmModelConfig("mistral7b", 8192),
    SupportedModels.mistral_7B_v2:  LlmModelConfig("mistral7b", 32000),
    SupportedModels.dolphin_2_8_mistral_v02:  LlmModelConfig("dolphin-mistral", 32000),
    SupportedModels.hermes_2_pro_mistral:  LlmModelConfig("hermes-2-mistral", 32000),
    SupportedModels.mixtral_8x_7b:  LlmModelConfig("mixtral", 32000),
    SupportedModels.wizardLm2_7b:  LlmModelConfig("wizardlm2:7b", 8192),

    # https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md
    SupportedModels.llama3_8b:  LlmModelConfig("llama3", 8192),  # this is q4
    SupportedModels.llama3_8b_q8:  LlmModelConfig("llama3:8b-instruct-q8_0", 8192),
    SupportedModels.llama3_70b:  LlmModelConfig("llama3:70b-instruct-q4_K_M", 8192),
    SupportedModels.llama3_gradient:  LlmModelConfig("llama3-gradient:8b-instruct-1048k-q6_K", 32000),
    SupportedModels.phi3_medium:  LlmModelConfig("phi3:14b", 32000),
    # this is q4
    SupportedModels.qwen2_7b:  LlmModelConfig("qwen2", 128000),
}


class LlmConfigFactory:
    def __init__(self, llm_model_type: SupportedModels, prompt_token_length: int = 0):
        self.llm_model = llm_models_config[llm_model_type]
        self.llm_model_name = llm_models_config[llm_model_type].name
        self.llm_model_context_window_size = llm_models_config[llm_model_type].context_window - \
            prompt_token_length
