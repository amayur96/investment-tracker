import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../../.env.local')

def parse_openai_response(response_data):
    """
    Parse OpenAI API response to extract text content and token usage
    
    Args:
        response_data (dict): The full OpenAI API response
    
    Returns:
        dict: Dictionary containing 'text' and 'total_tokens'
    """
    try:
        # Extract text from output -> content -> text
        text = ""
        if 'output' in response_data and response_data['output']:
            # Get the first output item
            output_item = response_data['output'][0]
            if 'content' in output_item and output_item['content']:
                # Get the first content item
                content_item = output_item['content'][0]
                if 'text' in content_item:
                    text = content_item['text']
        
        # Extract total_tokens from usage -> total_tokens
        total_tokens = 0
        if 'usage' in response_data and 'total_tokens' in response_data['usage']:
            total_tokens = response_data['usage']['total_tokens']
        
        return {
            'text': text,
            'total_tokens': total_tokens
        }
    
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing OpenAI response: {e}")
        return {
            'text': "",
            'total_tokens': 0
        }

def get_openai_response(ticker):
    """
    Make a request to OpenAI API to get news related to a specific ticker
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        dict: API response from OpenAI
    """
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # API endpoint
    url = "https://api.openai.com/v1/responses"
    
    # Headers with authorization
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Request body
    data = {
        "model": "gpt-4.1",
        "input": f"Give me some news related to the {ticker} ticker"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request to OpenAI API: {e}")
        raise
    except ValueError as e:
        print(f"Error parsing response: {e}")
        raise

def get_ticker_news(ticker="AAPL"):
    """
    Convenience function to get news for a specific ticker
    
    Args:
        ticker (str): Stock ticker symbol, defaults to 'AAPL'
    
    Returns:
        dict: OpenAI API response with news
    """
    return get_openai_response(ticker)

def get_ticker_news_parsed(ticker="AAPL"):
    """
    Get news for a specific ticker and return parsed text and token usage
    
    Args:
        ticker (str): Stock ticker symbol, defaults to 'AAPL'
    
    Returns:
        dict: Dictionary containing 'text' and 'total_tokens'
    """
    full_response = get_openai_response(ticker)
    return parse_openai_response(full_response)

if __name__ == "__main__":
    # Test the function
    try:
        result = get_ticker_news("AAPL")
        #print("OpenAI API Response:")
        #print(result)
        
        # Test the parsing function
        print("\n" + "="*50)
        print("Parsed Response:")
        parsed = parse_openai_response(result)
        
        print("Text:")
        print(parsed['text'])
        print(f"\nTotal Tokens: {parsed['total_tokens']}")
        
    except Exception as e:
        print(f"Failed to get news: {e}")
