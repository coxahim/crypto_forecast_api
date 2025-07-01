import pandas as pd

SUPPORTED_COINS = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'ada': 'cardano',
    'sol': 'solana',
    'xrp': 'ripple',
    'sui': 'sui',
    'link': 'chainlink',
    'avax': 'avalanche-2',
    'ton': 'the-open-network',
    'apt': 'aptos',
    'near': 'near',
    'ena': 'ethena',
    'atom': 'cosmos',
    'op': 'optimism',
    'grt': 'the-graph',
    'ldo': 'lido-dao'
}

def extrapolate_regressors(df, periods=7):
    future_dates = [df['ds'].max() + pd.Timedelta(days=i) for i in range(1, periods + 1)]
    future = pd.DataFrame({'ds': future_dates})

    for col in ['volume', 'market_cap']:
        last_vals = df[col].tail(3).values
        slope = (last_vals[-1] - last_vals[0]) / 2 if len(last_vals) >= 3 else 0
        last_val = last_vals[-1] if len(last_vals) > 0 else 0
        extrapolated = [max(last_val + slope * i, 0) for i in range(1, periods + 1)]
        future[col] = extrapolated

    return pd.concat([df[['ds', 'volume', 'market_cap']], future], ignore_index=True)