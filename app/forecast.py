import requests
import pandas as pd
from prophet import Prophet
from app.utils import SUPPORTED_COINS, extrapolate_regressors

def get_ohlcv(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {'vs_currency': 'usd', 'days': '90'}
    response = requests.get(url, params=params)
    data = response.json()

    if 'prices' not in data:
        raise Exception("Invalid response from CoinGecko")

    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['volume'] = [v[1] for v in data['total_volumes']]
    df['market_cap'] = [m[1] for m in data['market_caps']]
    df['ds'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['y'] = df['price']
    return df[['ds', 'y', 'volume', 'market_cap']]

def make_forecast(df):
    model = Prophet(daily_seasonality=True, changepoint_prior_scale=0.5)
    model.add_seasonality(name='weekly', period=7, fourier_order=5)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model.add_regressor('volume')
    model.add_regressor('market_cap')

    df_full = df[['ds', 'y', 'volume', 'market_cap']].copy()
    future = extrapolate_regressors(df_full, periods=7)
    model.fit(df_full)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']].tail(7)

def get_forecast_data(symbol):
    coin_id = SUPPORTED_COINS.get(symbol.lower())
    if not coin_id:
        raise Exception(f"Unsupported symbol: {symbol}")
    df = get_ohlcv(coin_id)
    forecast_df = make_forecast(df)
    return forecast_df, df