# Invtment portfolio manager

By providing ticker codes for stocks in your portfolio, this system will generate advisory reports based on techical and finanical data. It will also run a portfolio check, with buy/hold/sell recommendations.

> Side note: One limitation is that the ticker has to be supported by YFinance. No problems for US stocks, but often other stocks are denoted by their market provider for example DNORD.CO where .CO stands for Copenhagen. Just search for the company on Yahoo Finance and use the ticker you find there.

[Example portfolio check](example_portfolio_advice_report.md)

## Tech

We use Ollama to manage, host and infrence local LLM models. We access Ollama via LlamaIndex.

## Warning

This project will download files to your disk (yfinance, SEC (US gov) etc.).

It will also generate Markdown files in a local folder.

## Setup

- Python 3.11.9
- `pip install -r requirements`
- Install ollama and pull models you want i.e. `ollama pull qwen2` (qwen model has 128k context window which makes life easier)
- Setup app.config with model name you want
- Type in your stocks in app.config
- Run with `python main.py`
- See app.log for errors and information on run
- Ouput is Markdown files in folder `./reports/`

# Ideas

An investment portfolio manager that be used to analyse and advise on investments in a portfolio.

## Features

- Portfolio management
- Investment analysis
- Advice on investment decisions
- Analysis of investment performance
- Tracking of investment performance
- Reporting of investment performance
- Tracking of investment performance

## Resources

- SEC filings api limits requests 10/min. However, since LLMs are slow, it's not a problem.
- FMP (Not implemented) _We provide one of the most accurate financial data available on the market. You can get historical prices, fundamental data, insider transactions, and much more that goes back 30 years in history._ [FMP](https://site.financialmodelingprep.com/developer/docs)
- (Not implemented) [Finnhub Stock API](https://finnhub.io/)
- [YFinance](https://pypi.org/project/yfinance/) OS Python interface found [here](https://github.com/ranaroussi/yfinance)

# System design

## Techical data analysist

Will analyse a stock's historical performance.
Provided a dataframe with techical data,
this will analyse realities about trend, momentum, volatility, etc.

### Output

Will generate a report (markdown format) containing:

- Stock price.
- Stock performance numbers.
- Stock ytd growth.
- Techical indicators (SMA, MACD, ADX, RSI etc.).

## Financial statement analyst

Analyse a company's historical price data and provide insights into its performance.
Provide perspctives for the stock's future pricing. Moving average, Momentum etc.

### Output

Will generate a report (markdown format) containing perspectives on:

- Profitability.
- Growth.
- Upside and downside risk.
- Market and competition.

## Advisor

Based on input from 'Financial statement analyst' (finanicals) and 'Techical data analysist' (techical data), this will try to figure out if the company will be profitable and is worth investing in.

### Output

Report containing:

- Is the company profitable?
- Is there harmoy between technical indicators and financials?
- What are the sort term risk and long term?
- What are the riskfactors, i.e. geopolitical, macro, cyclical, technology, compitition, finanical trends.
- Buy/Hold/Sell rating.

# Architecture

High-Level Architecture, describes the components and their relationships. And the system is designed this way.
Basically we are looking for single responibility, modularity, loose coupling - that opens up for scalability. It's overkill, but it's a good principle.
Smaller components also open up for easier and more maintainable testing. Both unit- and integration tests.

## Controller

The controller orchestrates the workflow from data fetching to report generation. At this layer we can also build in error tolerance and logging.

## Data Acquisition Layer

_Responsible for fetching data from external APIs._

This layer will include classes to fetch data from different sources like SEC filings, FMP, Finnhub, and YFinance. Implementation specific processing and scrubbing might be done here.

DataFetcher (Abstract Base Class): Defines the interface for fetching data.
SECDataFetcher, FMPDataFetcher, FinnhubDataFetcher, YFinanceDataFetcher: Concrete implementations for fetching data from respective APIs.

## Analysis Layer

_Analyzes technical stock data._

This layer will analyze the fetched data and provide insights.

### Technical Data Analyst

Analyzes technical stock data. We look for momentum, price direction and try to asses short to medium term movement in price.

### Financial Statement Analyst

Analyzes financial statements. We look at key fundamentals, company's profitability and market conditions. We try to asses the quality of the buisness, from reported realities.

## Advisory Layer

This layer combines insights from both analysts to provide investment advice.

## Reporting Layer

Generates markdown reports based on the analyses and advice.

# Notes about the architecture

Here are some ideas about why the architecture is structured the way it is.

The system is modular - so it can be maintainable. We can develop and test each component independently. New features can be added with minimal changes to existing code.

**Single Responsibility Principle:** Each class has a single responsibility, such as fetching data, analyzing data, providing advice, or generating reports. Avoid big classes that can do everything.

**Open/Closed Principle:** It's easier to add new code. Classes are open for extension (e.g., adding new data fetchers or analysis methods) but closed for modification. For example: we don't have to rewrite a lot of things if we want to add new fetchers.

**Interface Segregation Principle:** Interfaces (e.g. DataFetcher) are clear and specific to the systems needs.

**Dependency Injection Principle:** Although it's a simplification in this app, the abstract interface locks in the "form of the api", but we still have the freedom to inject required resources via constructor on data fetchers.
For example: we give the StockInformationProcessor a llm configuration factory, instead of hardcoding the whole thing in that class. That makes it possible to create other processor classes, that can reuse the existing code.

**Dependency Inversion Principle:** High level modules (e.g., StockInformationProcessor) depend on abstractions (e.g., DataFetcher) rather than concrete implementations. Things can be more modular, even though it's not quite needed here. This decouples the processor from the underlying suppliers of data. It dosn't need to know about concrete implementations, it just needs to know it can get data (in a known format) from them.
