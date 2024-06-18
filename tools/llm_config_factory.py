from enum import Enum
from typing import Dict


class LlmModelConfig:
    def __init__(self, name, context_window):
        self.name = name
        self.context_window = context_window


class LlmModelType(Enum):
    default = 0
    techical = 1
    finanical = 2
    advisory = 3
    healthcheck = 4
    summarizer = 5


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
    phi3_3b = 14


# Før man kan bruge andre modeller skal man hente dem via "ollama pull <modelname>"
llm_models_config = {
    SupportedModels.mistral_7B_v1:  LlmModelConfig("mistral7b", 8192),
    SupportedModels.mistral_7B_v2:  LlmModelConfig("mistral7b", 32000),
    SupportedModels.dolphin_2_8_mistral_v02:  LlmModelConfig("dolphin-mistral", 32000),
    SupportedModels.hermes_2_pro_mistral:  LlmModelConfig("hermes-2-mistral", 32000),
    SupportedModels.mixtral_8x_7b:  LlmModelConfig("mixtral", 32000),
    SupportedModels.wizardLm2_7b:  LlmModelConfig("wizardlm2:7b", 8192),

    # https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md
    # this is q4 default
    SupportedModels.llama3_8b:  LlmModelConfig("llama3", 8192),
    SupportedModels.llama3_8b_q8:  LlmModelConfig("llama3:8b-instruct-q8_0", 8192),
    SupportedModels.llama3_70b:  LlmModelConfig("llama3:70b-instruct-q4_K_M", 8192),
    SupportedModels.llama3_gradient:  LlmModelConfig("llama3-gradient:8b-instruct-1048k-q6_K", 32000),
    SupportedModels.phi3_medium:  LlmModelConfig("phi3:14b", 128000),
    SupportedModels.phi3_3b:  LlmModelConfig("phi3", 4000),  # q4 default

    # this is q4 default
    SupportedModels.qwen2_7b:  LlmModelConfig("qwen2", 128000),
}


class LlmConfigFactory:
    def __init__(self, llm_model_config: Dict[str, str]):
        self.llm_model_config = llm_model_config

    def getModel(self, modelType: LlmModelType) -> LlmModelConfig:
        if (modelType == LlmModelType.techical):
            llm_key = self.llm_model_config["llm_model_techical"]
            model = SupportedModels[str(llm_key).lower()]
            conf = llm_models_config[model]
            return conf
        if (modelType == LlmModelType.finanical):
            return llm_models_config[SupportedModels[str(self.llm_model_config["llm_model_financial"]).lower()]]
        if (modelType == LlmModelType.advisory):
            return llm_models_config[SupportedModels[str(self.llm_model_config["llm_model_advisor_stock"]).lower()]]
        if (modelType == LlmModelType.healthcheck):
            return llm_models_config[SupportedModels[str(self.llm_model_config["llm_model_advisor_healthcheck"]).lower()]]
        if (modelType == LlmModelType.summarizer):
            return llm_models_config[SupportedModels[str(self.llm_model_config["llm_model_report_summarizer"]).lower()]]
        raise Exception("Invalid model type")
