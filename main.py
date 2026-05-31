import requests
import time

BOT_TOKEN = "8956939625:AAHKFs9p7ldLWegmqzhYNWRjK4tb8yBI-3w"
CHANNEL = "@mywishsingal"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": text, "parse_mode": "HTML"})

def get_price(symbol):
    try:
        if symbol in ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}=X"
        elif symbol == "XAUUSD":
            url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
        else:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=10)
        data = r.json()
        if symbol in ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]:
            return float(data["chart"]["result"][0]["meta"]["regularMarketPrice"])
        else:
            return float(data["price"])
    except:
        return None

def analyze_signal(price, symbol):
    import random
    action = random.choice(["BUY", "SELL"])
    
    if symbol == "BTCUSDT":
        sl = round(price * 0.02, 2)
        tp1 = round(price * 0.03, 2)
        tp2 = round(price * 0.05, 2)
    elif symbol == "ETHUSDT":
        sl = round(price * 0.025, 2)
        tp1 = round(price * 0.035, 2)
        tp2 = round(price * 0.06, 2)
    elif symbol in ["EURUSD", "GBPUSD"]:
        sl = round(price * 0.003, 5)
        tp1 = round(price * 0.005, 5)
        tp2 = round(price * 0.008, 5)
    elif symbol == "XAUUSD":
        sl = round(price * 0.008, 2)
        tp1 = round(price * 0.012, 2)
        tp2 = round(price * 0.02, 2)
    else:
        sl = round(price * 0.02, 4)
        tp1 = round(price * 0.03, 4)
        tp2 = round(price * 0.05, 4)
    
    if action == "BUY":
        sl_price = round(price - sl, 4)
        tp1_price = round(price + tp1, 4)
        tp2_price = round(price + tp2, 4)
    else:
        sl_price = round(price + sl, 4)
        tp1_price = round(price - tp1, 4)
        tp2_price = round(price - tp2, 4)
    
    return action, sl_price, tp1_price, tp2_price

PAIRS = {
    "BTCUSDT": "BTC/USDT",
    "ETHUSDT": "ETH/USDT", 
    "BNBUSDT": "BNB/USDT",
    "SUIUSDT": "SUI/USDT",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "XAUUSD": "XAU/USD (Gold)",
}

TIMEFRAMES = ["15M", "30M", "1H", "4H"]

def send_all_signals():
    for symbol, name in PAIRS.items():
        price = get_price(symbol)
        if not price:
            continue
        for tf in TIMEFRAMES:
            action, sl, tp1, tp2 = analyze_signal(price, symbol)
            emoji = "🟢" if action == "BUY" else "🔴"
            msg = f"""{emoji} <b>{action} SIGNAL</b>
📊 Pair: <b>{name}</b>
⏱ Timeframe: <b>{tf}</b>
💰 Entry: <b>{price}</b>
🛡 Stop Loss: <b>{sl}</b>
🎯 TP1: <b>{tp1}</b>
🎯 TP2: <b>{tp2}</b>
📢 @mywishsingal"""
            send_message(msg)
            time.sleep(3)

while True:
    send_all_signals()
    time.sleep(3600)