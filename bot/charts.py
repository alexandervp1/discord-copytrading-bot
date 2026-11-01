import io
import pandas as pd
import matplotlib 
matplotlib.use('Agg')
import mplfinance as mpf
import ccxt

binance = ccxt.binance()

def get_chart(symbol: str = "BTC/USDT", interval: str = "1d", limit: int = 90):
    ohlcv = binance.fetch_ohlcv(symbol, interval, limit=limit)
    df = pd.DataFrame(ohlcv, columns = ["Date","Open", "High", "Low", "Close", "Volume"])
    df["Date"] = pd.to_datetime(df["Date"], unit="ms")
    df = df.set_index("Date")

    buf = io.BytesIO() # for data streams
    mpf.plot(
        df,
        type="candle",
        style="nightclouds",
        volume=True,
        title=f'{symbol}  {interval}',
        savefig=dict(fname=buf, dpi=100, format="png")

    )
    buf.seek(0)
    return buf
