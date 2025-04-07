import pandas as pd
import tabulate
import yfinance as yf
import pandas_ta as ta
from tabulate import tabulate


# Tools for getting stock data from Yahoo Finance.
# Including simple techical analysis.

yfin_allowed_timespans = ['1d', '5d', '1mo', '3mo',
                          '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

yfin_allowed_intervals = ['1m', '2m', '5m', '15m', '30m',
                          '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


def get_essential_info(data: yf.Ticker) -> dict:
    inf = {}
    inf["Name"] = data.info.get("longName")
    inf["Industry"] = data.info.get("industryDisp")
    inf["Sector"] = data.info.get("sectorDisp")
    inf["Business Summary"] = data.info.get("longBusinessSummary")
    inf["Forward PE Ratio"] = data.info.get("forwardPE")
    inf["Beta"] = data.info.get("beta")
    inf["Current Price"] = data.info.get('currentPrice')
    inf["Target High Price"] = data.info.get('targetHighPrice')
    inf["Target Low Price"] = data.info.get('targetLowPrice')
    inf["Target Mean Price"] = data.info.get('targetMeanPrice')
    inf["Target Median Price"] = data.info.get('targetMedianPrice')
    inf["Recommendation Mean"] = data.info.get('recommendationMean')
    inf["Recommendation Key"] = data.info.get('recommendationKey')
    inf["Number of Analyst Opinions"] = data.info.get(
        'numberOfAnalystOpinions')
    inf["Short Ratio"] = data.info.get("shortRatio")
    inf["Previous Close"] = data.fast_info.previous_close
    inf["Day High"] = data.fast_info.day_high
    inf["Day Low"] = data.fast_info.day_low
    inf["Last Volume"] = data.fast_info.last_volume
    inf["50-day Moving Average"] = data.fast_info.fifty_day_average
    inf["200-day Moving Average"] = data.fast_info.two_hundred_day_average
    inf["Year High"] = data.fast_info.year_high
    inf["Year Low"] = data.fast_info.year_low
    inf["Year-to-Date Change"] = data.fast_info.year_change
    return inf


def round_dataframe_to_3dec(df):
    return df.round(3)


def remove_dataframe_nan(df):
    return df.dropna(how='all')


def get_yf_data(ticker) -> yf.Ticker:
    """
    Fetches stock data for the given ticker using yfinance.
    :param ticker: Stock ticker symbol as a string.
    :return: DataFrame with stock data.
    """
    # yf.enable_debug_mode()
    # Fetch data
    data = yf.Ticker(ticker)
    return data


def fetch_stock_history_data(yf_ticker_data) -> pd.DataFrame:

    # Get historical market data for the last n months
    df = yf_ticker_data.history(
        period=yfin_allowed_timespans[3], interval=yfin_allowed_intervals[8])

    # Ensure the DataFrame index is a DatetimeIndex
    df.index = pd.DatetimeIndex(df.index)

    return df


def techical_analysis(df: pd.DataFrame):
    """
    Performs technical analysis on the stock data using pandas_ta.

    :param df: DataFrame with stock data.
    :return: DataFrame with analysis results.
    """
    # Calculate Simple Moving Averages
    sma_short = ta.sma(df['Close'], length=10)
    df['SMA_10'] = sma_short
    sma_long = ta.sma(df['Close'], length=50)
    df['SMA_50'] = sma_long
    df['Golden Cross'] = (
        sma_short > sma_long) if sma_short is not None and sma_long is not None else pd.NA

    # Calculate MACD
    macd = ta.macd(df['Close'])
    if macd is not None and 'MACD_12_26_9' in macd.columns:
        df = df.join(macd)  # Join the MACD result with the main DataFrame
    else:
        # Initialize MACD columns to NaN if the calculation fails
        df['MACD'] = pd.NA
        df['MACDh'] = pd.NA
        df['MACDs'] = pd.NA

    # Calculate ADX
    adx = ta.adx(df['High'], df['Low'], df['Close'])
    if adx is not None:
        df = df.join(adx)

    # Calculate RSI
    df['RSI'] = ta.rsi(df['Close'])

    # Drop unnecessary columns
    df = df.drop(columns=["Open", "High", "Low",
                 "Dividends", "Stock Splits"], axis=1)
    # Drop data from early dates since calculations are not setteled on those (i.e. avg)
    df = df.tail(25)
    return df


def process_analysis_results(df):
    """
    Processes analysis results to generate buy or sell recommendations.

    :param df: DataFrame with analysis results.
    :return: Recommendations as a list of tuples (date, recommendation).
    """
    # Initialize an empty list for recommendations
    recommendations = []

    # Example logic to generate recommendations based on SMA crossover
    for index, row in df.iterrows():
        if pd.notnull(row['SMA_50']) and pd.notnull(row['SMA_200']):
            if row['SMA_50'] > row['SMA_200']:
                recommendations.append((index, 'Buy'))
            elif row['SMA_50'] < row['SMA_200']:
                recommendations.append((index, 'Sell'))
        else:
            # Handle cases where SMA values are NaN
            recommendations.append((index, 'Hold/No Recommendation'))

    return recommendations


def hum_stock_analyzer_tool(ticker_symbol: str) -> tuple[dict, list[pd.DataFrame]]:
    """Returns human readable dataframe, with the results of the techical indicators."""
    yf_ticker_data: yf.Ticker = get_yf_data(ticker_symbol)
    price_history: pd.DataFrame = fetch_stock_history_data(yf_ticker_data)

    analyst_recommendations = yf_ticker_data.get_recommendations_summary()
    if isinstance(analyst_recommendations, dict):
        analyst_recommendations = pd.DataFrame([analyst_recommendations])

    history_with_ta: pd.DataFrame = techical_analysis(price_history)

    # data.balance_sheet.loc[['Total Assets',
    #                         'Current Assets',
    #                         'Working Capital',
    #                         'Total Debt',
    #                         'Total Non Current Liabilities Net Minority Interest']]

    # columns_to_display = ['Open', 'High', 'Low', 'Close', 'Volume', 'Golden Cross', 'SMA_50',
    #                       'SMA_200', 'MACD_12_26_9', 'ADX_14', 'RSI_14']
    # existing_columns = [
    #     col for col in columns_to_display if col in df_with_analysis.columns]
    # ta_table = tabulate(df_with_analysis[existing_columns].tail(
    #     50), headers='keys', tablefmt='psql', showindex=True)
    # rec_table = tabulate(recdtn_df, headers='keys',
    #                      tablefmt='psql', showindex=True)

    info = get_essential_info(yf_ticker_data)

    trimmed_history = round_dataframe_to_3dec(
        remove_dataframe_nan(history_with_ta))
    arr = [trimmed_history, analyst_recommendations]

    return (info, arr)


"""
    | Metric | Description |
    | --- | --- |
    | Total assets | The total value of all assets owned by the company. This includes both current and non-current (long-term) assets. |
    | Current assets | Cash, accounts receivable, inventory, and other assets that are expected to be converted into cash within one year or the operating cycle, whichever is longer. These assets help in short-term financial operations. |
    | Shareholders' equity | The amount of money invested by shareholders (share owners) in a company, calculated as total assets minus liabilities. This represents the residual interest or ownership percentage of the shareholders in the company. |
    | Operating cash flow | The net cash generated from operating activities, which includes revenue-generating core business operations and excludes financing and investing activities. It shows how much cash a company generates from its normal business operations. |
    | Net cash flow | The net increase or decrease in cash during a specific period, calculated as the sum of cash flows from operating, investing, and financing activities. A positive number indicates an increase in cash, while a negative number represents a decrease. |
    | Total revenue | The total income generated by a company through its primary business activities, including sales, services, or other sources of income. This is the top line on an income statement and serves as the starting point for calculating a company's profitability. |
    | Gross profit | The difference between total revenue and cost of goods sold (COGS). It represents the profit a company makes after accounting for the direct costs associated with producing its products or services. |
    | Operating income | The profit earned from a company's core business operations, calculated as gross profit minus operating expenses such as selling, general, and administrative expenses. This metric helps assess a company's operational efficiency. |
    | Net income | The final profit of a company after accounting for all expenses, including taxes, interest, and other non-operating items. It represents the bottom line on an income statement and is the most widely used measure of a company's profitability. |

    These metrics provide a concise overview of a company's financial health and performance, focusing on the most critical aspects that an analyst would typically analyze in their assessments.
"""


def get_financial_numbers(ticker_symbol: str) -> tuple[dict, list[pd.DataFrame]]:
    """Returns dict with company info and tables with financial numbers."""
    data = yf.Ticker(ticker_symbol)
    info = get_essential_info(data)

    # 5 years of balance sheets
    five_yearbalance = data.balance_sheet.loc[['Total Assets',
                                               'Current Assets',
                                               'Working Capital',
                                               'Total Debt',
                                               'Total Non Current Liabilities Net Minority Interest']]

    # 4 latest quarter's balance sheet
    four_quater_balance = data.quarterly_balance_sheet.iloc[:, 0:4]
    four_quater_balance = four_quater_balance.loc[['Total Assets',
                                                   'Current Assets',
                                                   'Working Capital',
                                                   'Total Debt',
                                                   'Total Non Current Liabilities Net Minority Interest']]

    # Cash Flow
    columns_to_include = ['Free Cash Flow', 'Capital Expenditure', 'Operating Gains Losses',
                          'Operating Cash Flow', 'Beginning Cash Position', 'End Cash Position']
    # Skip columns that are not found
    existing_columns = data.cash_flow.index.intersection(columns_to_include)
    five_year_cash_flow = data.cash_flow.loc[existing_columns]

    four_quater_cash_flow = data.quarterly_cash_flow.iloc[:, 0:4]

    columns_to_include = [
        'Free Cash Flow',
        'Capital Expenditure',
        'Operating Gains Losses',
        'Operating Cash Flow',
        'Beginning Cash Position',
        'End Cash Position'
    ]

    existing_columns = four_quater_cash_flow.index.intersection(
        columns_to_include)
    four_quater_cash_flow = four_quater_cash_flow.loc[existing_columns]

    # Income Statement
    columns_to_include = [
        "Total Revenue",
        "Gross Profit",
        "Operating Income",
        "Net Income"
    ]

    existing_columns = data.income_stmt.index.intersection(columns_to_include)
    five_year_income = data.income_stmt.loc[existing_columns]

    columns_to_include = [
        "Total Revenue",
        "Gross Profit",
        "Operating Income",
        "Net Income"
    ]
    four_quater_income: pd.DataFrame = data.quarterly_income_stmt.iloc[:, 0:4]
    existing_columns = four_quater_income.index.intersection(
        columns_to_include)

    four_quater_income = data.quarterly_income_stmt.loc[existing_columns]

    yearly_metrics_df = pd.concat(
        [five_yearbalance, five_year_cash_flow, five_year_income], axis=1)

    quater_metrics_df = pd.concat(
        [four_quater_balance, four_quater_cash_flow, four_quater_income], axis=1)

    return (info, [round_dataframe_to_3dec(remove_dataframe_nan(yearly_metrics_df)),
                   round_dataframe_to_3dec(remove_dataframe_nan(quater_metrics_df))])
