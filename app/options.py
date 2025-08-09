from api import get_ticker_details

def get_options_contracts(underlying_ticker):
    """Get all options contracts for a given underlying ticker"""
    contracts = get_ticker_details(underlying_ticker, "option_contracts")
    return contracts

def get_options_contract(underlying_ticker):
    """
    Get specific fields from options contracts data for a given underlying ticker.
    
    Returns a list of dictionaries containing:
    - contract_type
    - exercise_style
    - expiration_date
    - strike_price
    - primary_exchange
    - underlying_ticker
    """
    contracts_data = get_options_contracts(underlying_ticker)
    
    if not contracts_data or 'results' not in contracts_data:
        print(f"No contracts data found for {underlying_ticker}")
        return []
    
    extracted_contracts = []
    
    for contract in contracts_data['results']:
        extracted_contract = {
            'contract_type': contract.get('contract_type'),
            'exercise_style': contract.get('exercise_style'),
            'expiration_date': contract.get('expiration_date'),
            'strike_price': contract.get('strike_price'),
            'primary_exchange': contract.get('primary_exchange'),
            'underlying_ticker': contract.get('underlying_ticker')
        }
        extracted_contracts.append(extracted_contract)
    
    return extracted_contracts

if __name__ == "__main__":
    # Test the function
    #result = get_options_contract("AAPL")
    result = get_options_contract("FIG")
    print("Extracted options contract data:")
    for i, contract in enumerate(result):
        print(f"Contract {i+1}: {contract}")
    
