from enum import Enum


class LlmModelConfig:
    def __init__(self, name, context_window):
        self.name = name
        self.context_window = context_window


class SupportedModels(Enum):
    Mistral_7B_v1 = 1
    Mistral_7B_v2 = 2
    Dolphin_2_8_mistral_v02 = 3
    Hermes_2_Pro_Mistral = 4
    Gemma_1_1_it = 5
    Mixtral_8x_7b = 6
    WizardLm2_7b = 7
    Llama3_8b = 8
    Llama3_70b = 9
    Llama3_gradient = 10
    Phi3_medium = 11


# Før man kan bruge andre modeller skal man hente dem via "ollama pull <modelname>"
llm_models_config = {
    SupportedModels.Mistral_7B_v1:  LlmModelConfig("mistral7b", 8192),
    SupportedModels.Mistral_7B_v2:  LlmModelConfig("mistral7b", 32000),
    SupportedModels.Dolphin_2_8_mistral_v02:  LlmModelConfig("dolphin-mistral", 32000),
    SupportedModels.Hermes_2_Pro_Mistral:  LlmModelConfig("hermes-2-mistral", 32000),
    SupportedModels.Mixtral_8x_7b:  LlmModelConfig("mixtral", 32000),
    SupportedModels.WizardLm2_7b:  LlmModelConfig("wizardlm2:7b", 8192),

    # https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md
    SupportedModels.Llama3_8b:  LlmModelConfig("llama3:8b-instruct-q8_0", 8192),
    SupportedModels.Llama3_70b:  LlmModelConfig("llama3:70b-instruct-q4_K_M", 8192),
    SupportedModels.Llama3_gradient:  LlmModelConfig("llama3-gradient:8b-instruct-1048k-q6_K", 32000),
    SupportedModels.Phi3_medium:  LlmModelConfig("phi3:14b", 32000),
}


class LlmConfigFactory:
    def __init__(self, llm_model_type: SupportedModels, prompt_token_length: int = 0):
        self.llm_model = llm_models_config[llm_model_type]
        self.llm_model_name = llm_models_config[llm_model_type].name
        self.llm_model_context_window_size = llm_models_config[llm_model_type].context_window - \
            prompt_token_length

# current_llm_model_key =
