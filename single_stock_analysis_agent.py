from agents.critics.stock_report_agent import StockReportAgent
from infrence_provider.infrence_provider_factory import InferenceProviderFactory
from portfolio_item import PortfolioItem
from stock_information_processor import StockInformationProcessor
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


# def main():
#     report_text = """
#     <think>
# Alright, so I'm trying to analyze the stock of Advanced Micro Devices (AMD) using the data provided. Let me start by understanding what each part of the data means and how it can help me make sense of the stock's performance.


# First, looking at the basic info: the current price is $114.6723, which seems a bit high compared to some other stocks I've seen. The target high is $250, but that might be more of an aspirational figure rather than something realistic right now. The target mean price is around $171.70, so maybe the analysts expect it to stabilize there in the long run.


# The recommendation mean is 1.7755 with a key buy rating. That suggests that on average, the buy signal is strong enough for investors to consider buying the stock. But I should check if this recommendation has changed recently or if it's based on historical data.


# Looking at the technical indicators: MACD_12_26_9 shows a negative value, which usually indicates a bearish trend. The MACDh_12_26_9 is also negative, suggesting that the short-term momentum is downward. The RSI is 24.66, which is below 30, indicating potential overselling and maybe an upward reversal.


# The SMA_50 is currently at $129.03, slightly above the current price of ~$114.67. This might mean that in the short term, the stock could be undervalued relative to its longer-term average. However, the 200-day moving average is higher at around $148.95, which suggests that over a year, the stock has been performing well.


# Looking at the volume, it's quite high on some days and lower on others. High volume can indicate strong interest or sentiment, but I need to see if these volumes correspond with price movements. For example, when the stock went up from ~$115 to $120 over a few days, the volume was also increasing, which might be positive.


# The ADX_14 is 38.65, which measures market strength. Values above 25 indicate a strong trend, so this suggests that AMD's stock has a solid upward trend. The DMP_14 and DMN_14 are both at 9.576 and 36.613 respectively, indicating a bullish trend in the short term.


# The YFinance data shows a forward PE ratio of 22.33, which is relatively low compared to its historical average, suggesting that the stock might be undervalued. The Beta is 1.706, meaning it's more volatile than the market; if the market goes up by 1%, AMD could go up by 1.7%.


# Looking at the price history over the past month, there are significant fluctuations. The stock peaked around $125 in early December and has dipped down to about $114 recently. This volatility might be due to various factors like earnings reports or industry developments.


# The strongBuy signal is active on 0m (the last five days), which means it's a good time to consider buying the stock based on these indicators. The buy signal was also active in the past month, indicating sustained positive momentum.


# In terms of performance, over the past year, AMD has increased by about -0.35%, which is slightly negative but not drastically so. This might be due to mixed earnings or some sector-specific issues within the company.


# Putting this all together, while there are some concerns like high volatility and a relatively low PE ratio compared to its peers, the overall trend is bullish with strong technical indicators pointing upwards. The buy recommendations from analysts also support the idea that now could be a good time to invest in AMD.


# </think>


# **Advanced Micro Devices (AMD) Technical Analysis Report**


# **Current Stock Price:** $114.67


# **Target High Price:** $250.00


# **Target Mean Price:** $171.70


# **Recommendation Mean:** 1.78 (Buy)


# ---


# ### Key Observations:


# 1. **Technical Indicators:**


#    - **MACD_12_26_9:** Negative (-5.454), indicating a bearish trend.


#    - **MACDh_12_6_9:** Negative (-0.393), suggesting short-term momentum is downward.


#    - **RSI (14):** 24.66, showing potential overselling and possible upward reversal.


#    - **SMA_50:** $129.03, slightly above current price, indicating undervaluation relative to longer-term average.


#    - **SMA_200:** $148.95, suggesting strong performance over the past year.


# 2. **Volume Analysis:**


#    - High volume observed on recent trading days, correlating with price movements upwards (e.g., from ~$115 to $120).


#    - Lower volumes on some days may indicate reduced interest or uncertainty.


# 3. **Market Sentiment:**


#    - **ADX_14:** 38.65, indicating a strong trend.


#    - **DMP_14/DMN_14:** 9.576 and 36.613 respectively, suggesting bullish momentum in the short term.


# 4. **Financial Metrics:**


#    - **Forward PE Ratio:** 22.33, relatively low compared to peers, implying potential undervaluation.


#    - **Beta:** 1.706, indicating higher volatility than the market; expected sensitivity to market movements.


# 5. **Price Performance Over Past Month:**


#    - Significant fluctuations with peaks around $125 and recent lows at ~$114, reflecting market sentiment and company news.


# 6. **Recommendations:**


#    - Strong buy signal active on 0m (last five days) and in the past month.


#    - Analysts' recommendations suggest sustained positive momentum.


# ---


# ### Conclusion:


# - **Current Sentiment:** Positive with a strong buy recommendation and bullish technical indicators, suggesting potential upside.


# - **Potential Risks:** High volatility and moderate PE ratio compared to peers should be monitored.


# - **Action Signal:** Given the strong buy signal and upward trend, this could be an opportune time to consider investing in AMD.


# **Final Rating:** Strong Buy


# **Investment Potential:** High

#     """


def main():
    # Expected string: {'name':'John Deere','ticker_symbol':'DE','buy_price':386.12,'currency':'USD','buy_date':'2024-06-18'}
    arg = sys.argv[1].replace("'", '"')
    # print(arg)
    jsonstr = json.loads(arg)
    stock = PortfolioItem(jsonstr)

    try:
        with open(os.path.join(config_path, "api_keys.json")) as keysFile:
            api_keys = json.load(keysFile)
    except FileNotFoundError as e:
        log.error(e)
    try:
        with open(os.path.join(config_path, "app_config.json")) as f:
            app_config = json.load(f)

    except FileNotFoundError as e:
        log.error(e)

    llm_provider = InferenceProviderFactory().create_provider(app_config)
    processor = StockInformationProcessor(api_keys, llm_provider)
    report_text: str = processor.process(stock)

    agent = StockReportAgent(llm_provider)
    finished_report = agent.hone_report(report_text)
    print(UnicodeSafety().makeSafe("REPORT:" + finished_report))


if __name__ == "__main__":
    main()
