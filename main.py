import requests
import time
import random

BOT_TOKEN = "8956939625:AAHKFs9p7ldLWegmqzhYNWRjK4tb8yBI-3w"
CHANNEL = "@mywishsingal"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": text, "parse_mode": "HTML"})

def get_signal(pair):
    actions = ["BUY", "SELL"]
    action = random.choice(actions)
    tp = round(random.uniform(0.5, 2.0), 2)
    sl = round(random.uniform(0.3, 1.0), 2)
    return action, tp, sl

def send_signals():
    pairs = ["BTC/USD", "EUR/USD", "GBP/USD", "XAU/USD", "USD/JPY"]
    for pair in pairs:
        action, tp, sl = get_signal(pair)
        emoji = "🟢" if action == "BUY" else "🔴"
        msg = f"""
{emoji} <b>{action} SIGNAL</b>
📊 Pair: <b>{pair}</b>
🎯 Take Profit: {tp}%
🛡 Stop Loss: {sl}%
⏰ Time: Now
📢 @mywishsingal
"""
        send_message(msg)
        time.sleep(2)

while True:
    send_signals()
    time.sleep(3600)
