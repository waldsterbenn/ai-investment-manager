import pandas as pd
import tabulate
import yfinance as yf
import pandas_ta as ta
from tabulate import tabulate


# Tools for getting stock data from Yahoo Finance.
# Including simple techical analysis.

yfin_allowed_timespans = ['1d', '5d', '1mo', '3mo',
                          '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']


def fetch_stock_data(ticker) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """
    Fetches stock data for the given ticker using yfinance.

    :param ticker: Stock ticker symbol as a string.
    :return: DataFrame with stock data.
    """
    # Fetch data
    data = yf.Ticker(ticker)
    # Get historical market data for the last n months
    df = data.history(period=yfin_allowed_timespans[4])

    # Ensure the DataFrame index is a DatetimeIndex
    df.index = pd.DatetimeIndex(df.index)

    return (data.info, df, data.get_recommendations_summary())


def analyze_stock(df):
    """
    Performs technical analysis on the stock data using pandas_ta.

    :param df: DataFrame with stock data.
    :return: DataFrame with analysis results.
    """
    # Calculate Simple Moving Averages
    sma50 = ta.sma(df['Close'], length=50)
    df['SMA_50'] = sma50
    sma200 = ta.sma(df['Close'], length=200)
    df['SMA_200'] = sma200
    df['Golden Cross'] = sma50 > sma200

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
    # print(df)
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

# not in use


def fu_stock_analyzer_tool(ticker_symbol: str) -> str:
    """Returns the name of the pickled pandas dataframe, with the results of the techical indicators."""
    (info, df) = fetch_stock_data(ticker_symbol)
    df_with_analysis = analyze_stock(df)
    pickle_filename = f"{ticker_symbol}_analysis.pkl"
    df_with_analysis.to_pickle(pickle_filename)
    print(f"DataFrame with analysis has been saved to {pickle_filename}.")
    return f"DataFrame with analysis has been saved to {pickle_filename}."


def hum_stock_analyzer_tool(ticker_symbol: str) -> tuple[dict, str]:
    """Returns human readable dataframe, with the results of the techical indicators."""
    (info, history_df, recdtn_df) = fetch_stock_data(ticker_symbol)
    df_with_analysis = analyze_stock(history_df)

    columns_to_display = ['Open', 'High', 'Low', 'Close', 'Volume', 'Golden Cross', 'SMA_50',
                          'SMA_200', 'MACD_12_26_9', 'ADX_14', 'RSI_14']
    existing_columns = [
        col for col in columns_to_display if col in df_with_analysis.columns]
    # ta_table = tabulate(df_with_analysis[existing_columns].tail(
    #     50), headers='keys', tablefmt='psql', showindex=True)
    # rec_table = tabulate(recdtn_df, headers='keys',
    #                      tablefmt='psql', showindex=True)

    df_with_analysis.columns = [
        f'TechicalData_{col}' for col in df_with_analysis.columns]
    recdtn_df.columns = [f'AnalystRating_{col}' for col in recdtn_df.columns]

    # Merge DataFrames on index
    df = pd.concat([df_with_analysis, recdtn_df], axis=1)
    df = df.dropna(how='all')
    return (info, df)


# def get_financial_numbers(ticker_symbol: str) -> str:
#     """Returns a dictionary with financial numbers."""
#     data = yf.Ticker(ticker_symbol)

#     balance = tabulate(data.balance_sheet, headers='keys',
#                        tablefmt='psql', showindex=True)
#     fin = tabulate(data.financials, headers='keys',
#                    tablefmt='psql', showindex=True)
#     inc = tabulate(data.income_stmt, headers='keys',
#                    tablefmt='psql', showindex=True)
#     return '#Balance\n'+balance+'\n\n#Financials\n'+fin+'\n\n#Income statement\n'+inc

def get_financial_numbers(ticker_symbol: str) -> pd.DataFrame:
    """Returns a dictionary with financial numbers."""
    data = yf.Ticker(ticker_symbol)

    balance = data.balance_sheet
    fin = data.financials
    return fin.dropna(how='all')
    inc = data.income_stmt

    # Add prefix to DataFrame columns to make them unique and clear
    balance.columns = [f'Balance_{col}' for col in balance.columns]
    fin.columns = [f'Financial_{col}' for col in fin.columns]
    inc.columns = [f'Income_{col}' for col in inc.columns]

    # Merge DataFrames on index
    df = pd.concat([balance, fin, inc], axis=1)

    # Convert DataFrame to markdown table
    # md_table = df.to_markdown(index=True)

    return df
