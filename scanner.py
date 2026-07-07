import yfinance as yf
import time

def load_watchlist(filename="watchlist.txt"):
with open(filename, "r") as f:
return [line.strip() for line in f if line.strip()]

def display_symbol(symbol):
if symbol == "^GSPC":
return "SPX"
if symbol == "BRK-B":
return "BRK.B"
return symbol

def scan_watchlist(symbols):
prices = {}
ema20 = {}
ema50 = {}

for symbol in symbols:
name = display_symbol(symbol)
try:
ticker = yf.Ticker(symbol)
price = ticker.fast_info["last_price"]
prices[name] = round(price, 2)

hist = ticker.history(period="5d", interval="5m")
ema20[name] = round(hist["Close"].ewm(span=20).mean().iloc[-1], 2)
