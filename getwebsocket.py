#download kline data from websocket for bitcoin as csv
import pandas as pd
import time
from pybit import WebSocket
subs = [
    "klineV2.1.BTCUSD"
]
ws = WebSocket(
    "wss://stream-testnet.bybit.com/realtime",
    subscriptions=subs
)
df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close"])

while True:
    data = ws.fetch(subs[0])
    if data:
        df = df.append(data, ignore_index=True)
        df.to_csv("kline.csv")
        time.sleep(1)