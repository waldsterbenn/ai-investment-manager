from agents.advisors.stock_advisor import StockAdvisor
from infrence_provider.infrence_provider_factory import InferenceProviderFactory
import logging.config
import logging
import json
import os
import sys
import base64

from tools.unicode_safety import UnicodeSafety

config_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), './config/'))

logging.config.fileConfig(os.path.join(config_path, "logging.config"))

# Get the logger specified in the configuration file
log = logging.getLogger('sampleLogger')


def main():
    # Expected string: {'TECHREPORT':'test','FINREPORT':'test'}
    arg = sys.argv[1]
    decoded_arg = base64.urlsafe_b64decode(arg + '===').decode()
    jsonstr = json.loads(decoded_arg)
    technical_analysis = jsonstr['TECHREPORT']
    financial_analysis = jsonstr['FINREPORT']

    try:
        with open(os.path.join(config_path, "app_config.json")) as f:
            app_config = json.load(f)

    except FileNotFoundError as e:
        log.error(e)

    llm_provider = InferenceProviderFactory().create_provider(app_config)
    stock_advisor = StockAdvisor(llm_provider)
    advice_on_stock = stock_advisor.provide_advice(
        technical_analysis, financial_analysis)

    print(UnicodeSafety().makeSafe("ADVICE:" + advice_on_stock))


if __name__ == "__main__":
    main()
