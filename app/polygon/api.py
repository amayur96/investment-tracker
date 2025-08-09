import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('../../.env.local')

# Get API key from environment
API_KEY = os.getenv('POLYGON_API_KEY')

def get_ticker_details(ticker):
    # Get ticker details
    url = f"https://api.polygon.io/v3/reference/tickers"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "ticker": ticker,
        "market": "stocks",
        "active": "true",
        "order": "asc",
        "limit": "5",
        "sort": "ticker"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")



def get_financial_statements_data(ticker):
    url = f"https://api.polygon.io/vX/reference/financials"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "ticker": ticker
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_financial_statement(statement_type, ticker):
    data = get_financial_statements_data(ticker)
    results = data["results"]
    financial_statements = results[0]["financials"]
    statement = None
    if statement_type == "cash_flow_statement":
        statement = financial_statements["cash_flow_statement"]
    elif statement_type == "income_statement":
        statement = financial_statements["income_statement"]
    else:
        statement = financial_statements["balance_sheet"]
    return statement

def get_statement_field(field_name, ticker, statement_type):
    statement = get_financial_statement(statement_type, ticker)
    return statement[field_name]["value"]


def get_gross_margin(ticker):
    gross_profit = get_statement_field("gross_profit", ticker, "income_statement")
    revenue = get_statement_field("revenues", ticker, "income_statement")
    gross_margin = round((gross_profit / revenue) * 100, 2)
    print(f"{ticker} Gross Margin: {gross_margin}%")
    return gross_margin

def get_financial_report(ticker):
    """
    Get key financial metrics for a ticker from the income statement.
    Returns a dictionary with Revenue, Gross Profit, Net Income, and Diluted EPS.
    """
    fields = {
        "Revenue": "revenues",
        "Gross Profit": "gross_profit",
        "Net Income": "net_income_loss",
        "Diluted EPS": "diluted_earnings_per_share",
    }
    
    report = {"Ticker": ticker}
    
    for label, field in fields.items():
        try:
            value = get_statement_field(field, ticker, "income_statement")
            # Format large numbers (in millions/billions) for readability
            if label in ["Revenue", "Gross Profit", "Net Income"] and value is not None:
                if value >= 1_000_000_000:
                    report[label] = f"${value/1_000_000_000:.2f}B"
                elif value >= 1_000_000:
                    report[label] = f"${value/1_000_000:.2f}M"
                else:
                    report[label] = f"${value:,.2f}"
            elif label == "Diluted EPS" and value is not None:
                report[label] = f"${value:.2f}"
            else:
                report[label] = "N/A"
        except Exception as e:
            print(f"Error getting {label} for {ticker}: {e}")
            report[label] = "N/A"
    
    return report
    
if __name__ == "__main__":
    #get_ticker_details("AAPL")
    #get_ticker_details("PLTR")
    get_gross_margin("AAPL")
    get_gross_margin("PLTR")
    get_gross_margin("TSLA")
    