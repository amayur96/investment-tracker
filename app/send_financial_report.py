import os
import time
from dotenv import load_dotenv
from api import get_financial_report
from email_client import send_email

load_dotenv('.env.local')

def create_html_table(ticker_reports):
    html = """
    <html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                max-width: 800px;
                margin: 20px auto;
                font-family: Arial, sans-serif;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            h2 {
                text-align: center;
                color: #333;
                font-family: Arial, sans-serif;
            }
            .number {
                text-align: right;
            }
        </style>
    </head>
    <body>
        <h2>Financial Report</h2>
        <table>
            <tr>
                <th>Ticker</th>
                <th>Revenue</th>
                <th>Gross Profit</th>
                <th>Net Income</th>
                <th>Diluted EPS</th>
            </tr>
    """
    
    for report in ticker_reports:
        html += f"""
            <tr>
                <td>{report['Ticker']}</td>
                <td class="number">{report['Revenue']}</td>
                <td class="number">{report['Gross Profit']}</td>
                <td class="number">{report['Net Income']}</td>
                <td class="number">{report['Diluted EPS']}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

def send_financial_report(to_email, tickers):
    ticker_reports = []
    
    print("Fetching financial data for tickers...")
    for i, ticker in enumerate(tickers):
        try:
            report = get_financial_report(ticker)
            ticker_reports.append(report)
            print(f"Successfully fetched data for {ticker}")
            # Add 10 second delay between API calls
            if i < len(tickers) - 1:
                print(f"Waiting 60 seconds before next request...")
                time.sleep(60)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            # Add error report with N/A values
            error_report = {
                'Ticker': ticker,
                'Revenue': 'N/A',
                'Gross Profit': 'N/A', 
                'Net Income': 'N/A',
                'Diluted EPS': 'N/A'
            }
            ticker_reports.append(error_report)
    
    html_content = create_html_table(ticker_reports)
    
    # Send email using the imported send_email function
    subject = 'Daily Stock Report'
    send_email(to_email, subject, html_content, html=True)
    print(f"Email sent successfully to {to_email}")

if __name__ == "__main__":
    tickers = ["META","AAPL", "MSFT", "GOOGL", "PLTR", "NVDA"]
    recipient = os.getenv('EMAIL_FROM')
    send_financial_report(recipient, tickers)