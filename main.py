import os
from dotenv import load_dotenv
from fastapi import FastAPI
import pandas as pd
import requests

# 1. Load the secret variables from .env
load_dotenv()

app = FastAPI()

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

# --- UPDATED: The Professional Greet & Home ---
@app.get("/")
def home():
    return {
        "welcome_msg": "Hello Souptik! Welcome to your Market Intelligence Engine.",
        "status": "Online",
        "key_status": "Loaded" if ALPHA_VANTAGE_KEY else "Missing",
        "available_endpoints": {
            "Analysis": "/market-report",
            "Personal Greeting": "/hello/{your_name}"
        }
    }

# --- ADDED: The Dynamic Greeting ---
@app.get("/hello/{name}")
def greet_user(name: str):
    return {
        "greeting": f"Hello {name}!",
        "message": "The engine is ready to process your financial data."
    }

@app.get("/market-report")
def get_market_report():
    try:
        # 1. Fetch NVIDIA Price
        nvda_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NVDA&apikey={ALPHA_VANTAGE_KEY}'
        nvda_response = requests.get(nvda_url)
        
        if nvda_response.status_code != 200:
            return {"error": f"Alpha Vantage down. Status: {nvda_response.status_code}"}
            
        nvda_data = nvda_response.json()
        nvda_price = float(nvda_data['Global Quote']['05. price'])

        # 2. Fetch Bitcoin Price
        btc_response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        
        if btc_response.status_code != 200:
            return {"error": f"CoinGecko down. Status: {btc_response.status_code}"}

        btc_data = btc_response.json()
        btc_price = float(btc_data['bitcoin']['usd'])

        # 3. Data Processing with Pandas
        data = {
            "Asset": ["NVIDIA", "Bitcoin"],
            "Price_USD": [nvda_price, btc_price]
        }
        df = pd.DataFrame(data)
        
        # Calculate the Ratio
        ratio = round(btc_price / nvda_price, 2)
        target_ratio = 100
        gap_percent = round(((ratio - target_ratio) / target_ratio) * 100, 2)

        return {
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market_data": df.to_dict(orient="records"),
            "analysis": {
                "nvda_btc_ratio": f"1 BTC = {ratio} NVDA Shares",
                "market_benchmark": f"Ratio is {gap_percent}% above the 100-share benchmark",
                "insight": "BTC is dominant" if ratio > 100 else "NVDA is closing the valuation gap"
            },
            "system_check": {
                "nvda_status": nvda_response.status_code,
                "btc_status": btc_response.status_code
            }
        }
    except Exception as e:
        return {"error": "Could not fetch live data.", "details": str(e)}