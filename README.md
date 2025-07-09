# Crypto Forecast API 🔮📊

This project is a deploy-ready cryptocurrency forecast and analytics API powered by [Facebook Prophet](https://facebook.github.io/prophet/), [FastAPI](https://fastapi.tiangolo.com/), and live data from [CoinGecko](https://www.coingecko.com/en/api).

It also includes a working [Telegram bot](https://core.telegram.org/bots/api) frontend for interacting with forecast results.

---

## 🚀 Features

✅ 7-day price forecasting using Prophet  
✅ OHLC visualization with volume and RSI  
✅ Live CoinGecko data for BTC, ETH, SOL, ADA, XRP  
✅ Backtest chart generator  
✅ Telegram bot interface with inline keyboard  
✅ Fully asynchronous FastAPI backend  
✅ Ready for deployment with `uvicorn`

---

## 🛠️ Stack

- Python 3.12
- FastAPI
- Prophet
- Matplotlib
- Pandas / NumPy
- CoinGecko API
- python-telegram-bot

---

## ⚙️ Run Locally

```bash
# Clone repository
git clone https://github.com/coxahim/crypto_forecast_api.git
cd crypto_forecast_api

# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
