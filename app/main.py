from fastapi import FastAPI, HTTPException
from app.forecast import get_forecast_data
from app.plot import generate_chart_base64

app = FastAPI(title="Crypto Forecast API")

@app.get("/forecast/{symbol}")
async def forecast(symbol: str):
    try:
        df_forecast, df_original = get_forecast_data(symbol)
        chart_b64 = generate_chart_base64(df_forecast, df_original, symbol)
        return {
            "symbol": symbol.upper(),
            "forecast": [
                {"date": row['ds'].strftime('%Y-%m-%d'), "price": round(row['yhat'], 4)}
                for i, row in df_forecast.iterrows()
            ],
            "chart_base64": chart_b64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))