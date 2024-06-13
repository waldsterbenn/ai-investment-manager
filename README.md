# Invtment portfolio manager

## Setup

- Python 3.11.9
- `pip install -r requirements`

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

- SEC filings 100 free requests (use browser agent for scraping) [SEC-API.io](https://sec-api.io/docs/query-api/financial-statements)
- FMP _We provide one of the most accurate financial data available on the market. You can get historical prices, fundamental data, insider transactions, and much more that goes back 30 years in history._ [FMP](https://site.financialmodelingprep.com/developer/docs)
- [Finnhub Stock API](https://finnhub.io/)
- [YFinance](https://pypi.org/project/yfinance/)

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
- Techical indicators (P/E, EPS, RSI etc.).

## Financial statement analyst

Will analyse a company's financial statements and provide insights into its performance.
Provided official financial statements and documents,
it will analyse the company's financial reality. And provide perspctives for the company's future.

### Output

Will generate a report (markdown format) containing:

- Profitability.
- Growth.
- Upside and downside risk.
- Market and competition.

## Advisor

Based on input from 'Financial statement analyst' (finanicals) and 'Techical data analysist' (techical data), this will try to figure out if the company will be profitable.

### Output

Report containing:

- Is the company profitable?
- Is there harmoy between technical indicators and financials?
- What are the sort term risk and long term?
- What are the riskfactors, i.e. geopolitical, macro, cyclical, technology, compitition, finanical trends.
- Buy or sell?

# Architecture

High-Level Architecture, describes the components and their relationships. And the system is designed this way.
Basically we are looking for single responibility, modularity, loose coupling - that opens up for scalability.
Smaller components also open up for easier and more maintainable testing. Both unit- and integration tests.

## Controller

The controller orchestrates the workflow from data fetching to report generation. At this layer we can also build in error tolerance and logging.

## Data Acquisition Layer

_Responsible for fetching data from external APIs._

This layer will include classes to fetch data from different sources like SEC filings, FMP, Finnhub, and YFinance.

DataFetcher (Abstract Base Class): Defines the interface for fetching data.
SECDataFetcher, FMPDataFetcher, FinnhubDataFetcher, YFinanceDataFetcher: Concrete implementations for fetching data from respective APIs.

## Analysis Layer

_Analyzes technical stock data._

This layer will analyze the fetched data and provide insights.

### Technical Data Analyst

Analyzes technical stock data.

### Financial Statement Analyst

Analyzes financial statements.

## Advisory Layer

This layer combines insights from both analysts to provide investment advice.

## Reporting Layer

Generates markdown reports based on the analyses and advice.

# Notes

Here are some ideas about why the architecture is structured the way it is.

The system is modular - so it can be maintainable. We can develop and test each component independently. New features can be added with minimal changes to existing code.

**Single Responsibility Principle:** Each class has a single responsibility, such as fetching data, analyzing data, providing advice, or generating reports. Avoid big classes that can do everything.

**Open/Closed Principle:** It's easier to add new code. Classes are open for extension (e.g., adding new data fetchers or analysis methods) but closed for modification.

**Interface Segregation Principle:** Interfaces (e.g. DataFetcher) are clear and specific to the systems needs.

**Dependency Injection Principle:** Although it's a simplification in this app, the abstract interface locks in the "form of the api", but we still have the freedom to inject required resources via constructor on data fetchers.

**Dependency Inversion Principle:** Highlevel modules (e.g., InvestmentPortfolioManager) depend on abstractions (e.g., DataFetcher) rather than concrete implementations. Things can be more modular, even though it's not quite needed here.
