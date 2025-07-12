import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('../.env.local')

# Get API key from environment
API_KEY = os.getenv('POLYGON_API_KEY')

def get_ticker_details(ticker):
    # Get ticker details for AAPL
    url = f"https://api.polygon.io/v3/reference/tickers"
    params = {
        "ticker": ticker,
        "market": "stocks",
        "active": "true",
        "order": "asc",
        "limit": "5",
        "sort": "ticker",
        "apiKey": API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_ticker_details("AAPL")
    get_ticker_details("PLTR")