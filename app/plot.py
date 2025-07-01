import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import io
import base64

def prepare_candles(df):
    df['date'] = df['ds'].dt.date
    grouped = df.groupby('date')['y']

    ohlc = pd.DataFrame()
    ohlc['open'] = grouped.first()
    ohlc['close'] = grouped.last()
    ohlc['high'] = grouped.max()
    ohlc['low'] = grouped.min()
    ohlc['volume'] = df.groupby('date')['volume'].sum()
    ohlc.index = pd.to_datetime(ohlc.index)
    return ohlc.reset_index()

def generate_chart_base64(forecast_df, original_df, symbol):
    ohlc_orig = prepare_candles(original_df)
    forecast_df_renamed = forecast_df.rename(columns={'yhat': 'y'})
    forecast_df_renamed['volume'] = original_df['volume'].mean()
    ohlc_forecast = prepare_candles(forecast_df_renamed)

    combined = pd.concat([ohlc_orig, ohlc_forecast], ignore_index=True)

    plt.style.use('dark_background')
    fig, (ax_price, ax_vol) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    dates = mdates.date2num(combined['date'])
    width = 0.6

    for i in range(len(combined)):
        o, c = combined['open'][i], combined['close'][i]
        h, l = combined['high'][i], combined['low'][i]
        date = dates[i]
        color = 'lime' if c >= o else 'red'
        ax_price.vlines(date, l, h, color=color, linewidth=1)
        ax_price.bar(date, abs(c - o), width, bottom=min(o, c), color=color, edgecolor='black')

    forecast_dates = mdates.date2num(ohlc_forecast['date'])
    ax_price.plot(forecast_dates, ohlc_forecast['close'], color='cyan', marker='o', linestyle='-', linewidth=2)

    y_last = combined['close'].iloc[-1]
    y_prev = combined['close'].iloc[-2]
    x_last = dates[-1]
    direction = np.sign(y_last - y_prev)
    arrow_color = 'lime' if direction >= 0 else 'red'
    ax_price.annotate('', xy=(x_last, y_last), xytext=(x_last, y_last - direction * 0.05 * y_last),
                      arrowprops=dict(facecolor=arrow_color, shrink=0.05, width=3, headwidth=8))

    ax_price.set_title(f"{symbol.upper()} 7-Day Forecast", color='white')
    ax_price.tick_params(colors='white')
    ax_price.grid(color='gray', linestyle='--', linewidth=0.3)

    ax_vol.bar(dates, combined['volume'], color='blue', width=width)
    ax_vol.tick_params(colors='white')
    ax_vol.grid(color='gray', linestyle='--', linewidth=0.3)

    ax_vol.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax_vol.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax_vol.xaxis.get_majorticklabels(), rotation=45, ha='right', color='white')

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64