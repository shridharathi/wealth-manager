import requests
import json
import os

POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')

def get_stock_data(ticker):
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/prev'
    headers = {
        'Authorization': f'Bearer {POLYGON_API_KEY}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    open = data["results"][0]["o"]
    close = data["results"][0]["c"]
    high = data["results"][0]["h"]
    low = data["results"][0]["l"]
    
    output = f"For {ticker}, the latest open price was {open}, the latest close price was {close}, the latest high price was {high}, and the latest low price was {low}."
    print(output)
    return output