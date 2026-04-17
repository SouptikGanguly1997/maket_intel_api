# 📈 Market Intelligence API
A high-performance backend engine that fetches real-time data for NVIDIA and Bitcoin, performing cross-asset analysis using Python and Pandas.

## 🚀 Key Features
- **Real-time Data:** Fetches live prices from Alpha Vantage and CoinGecko.
- **Data Engineering:** Uses Pandas for structured data transformation.
- **Security:** Implements `python-dotenv` for credential masking.
- **Error Handling:** Robust status code validation for network stability.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Framework:** FastAPI
- **Data Analysis:** Pandas
- **Server:** Uvicorn

## 🚦 How to Run
1. Clone this repo.
2. Create a `.env` file with your `ALPHA_VANTAGE_KEY`.
3. Run `python -m uvicorn main:app --reload`.