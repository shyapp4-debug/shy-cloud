import yfinance as yf
import csv
import os
import threading
from flask import Flask, render_template_string

app = Flask(__name__)

TRADE_LOG_FILE = "shy_trade_log.csv"

def start_shy_bot():
    # Importing qqq_bot starts the existing SHY scanning loop.
    import qqq_bot # noqa: F401

def load_trades():
    if not os.path.exists(TRADE_LOG_FILE):
        return []

    try:
        with open(TRADE_LOG_FILE, "r", newline="") as file:
            return list(csv.DictReader(file))
    except Exception as error:
        print("Dashboard trade-log error:", error)
        return []

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- <meta http-equiv="refresh" content="30"> -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SHY Trading Dashboard</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #101318;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1100px;
            margin: auto;
        }

        h1 {
            margin-bottom: 5px;
        }

        .subtitle {
            color: #aeb7c4;
            margin-bottom: 24px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
            margin-bottom: 25px;
        }

        .card {
            background: #1b2028;
            border: 1px solid #303743;
            border-radius: 12px;
            padding: 18px;
        }

        .label {
            color: #aeb7c4;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .value {
            font-size: 25px;
            font-weight: bold;
        }

        .table-box {
            overflow-x: auto;
            background: #1b2028;
            border: 1px solid #303743;
            border-radius: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 900px;
        }

        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #303743;
        }

        th {
            color: #aeb7c4;
            font-size: 13px;
        }

        .open {
            font-weight: bold;
        }

        .empty {
            padding: 28px;
            color: #aeb7c4;
        }
.market-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
    margin: 16px 0 28px;
}

.market-card {
    background: #182231;
    border: 1px solid #34445a;
    border-radius: 12px;
    padding: 16px;
}

.market-symbol {
    color: #9aa9bc;
    font-size: 14px;
    font-weight: bold;
}

.market-price {
    color: #ffffff;
    font-size: 25px;
    font-weight: bold;
    margin-top: 7px;
}

@media (max-width: 700px) {
    .market-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
    </style>
</head>

<body>
<div class="container">

    <h1>SHY Trading Dashboard</h1>
    <div class="subtitle">
        Automatically refreshes every 30 seconds
    </div>

    <div class="cards">
        <div class="card">
            <div class="label">Total Logged Trades</div>
            <div class="value">{{ total_trades }}</div>
        </div>

        <div class="card">
            <div class="label">Open Trades</div>
            <div class="value">{{ open_trades }}</div>
        </div>

        <div class="card">
            <div class="label">Latest Ticker</div>
            <div class="value">{{ latest_ticker }}</div>
        </div>

        <div class="card">
            <div class="label">Latest Grade</div>
            <div class="value">{{ latest_grade }}</div>
        </div>

        <div class="card">
            <div class="label">Latest Signal</div>
            <div class="value">{{ latest_signal }}</div>
            <div class="label">Entry: {{ latest_entry }}</div>
            <div class="label">Stop: {{ latest_stop }}</div>
            <div class="label">Target: {{ latest_target }}</div>
            <div class="label">Confidence: {{ latest_confidence }}%</div>
        </div>

        <div class="card">
            <div class="label">Market Bias</div>
            <div class="value">{{ market_bias }}</div>
            <div class="label">Score: {{ bias_score }}/3</div>
        </div>
        
<h2>Live Market Prices</h2>

<div class="market-grid">
    {% for symbol, price in live_prices.items() %}
    <div class="market-card">
        <div class="market-symbol">{{ symbol }}</div>

        <div class="market-price">
            {% if price == "Unavailable" %}
            {{ price }}
            {% else %}
                ${{ "%.2f"|format(price) }}
            {% endif %}
        </div>
    </div>
    {% endfor %}
</div>
 
<h2>Recent Trade Alerts</h2>

    <div class="table-box">
        {% if trades %}
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Ticker</th>
                    <th>Direction</th>
                    <th>Signal</th>
                    <th>Entry</th>
                    <th>Stop</th>
                    <th>Target</th>
                    <th>Grade</th>
                    <th>Confidence</th>
                    <th>Status</th>
                </tr>
            </thead>

            <tbody>
                {% for trade in trades %}
                <tr>
                    <td>{{ trade.get("timestamp", "") }}</td>
                    <td>{{ trade.get("ticker", "") }}</td>
                    <td>{{ trade.get("direction", "") }}</td>
                    <td>{{ trade.get("signal", "") }}</td>
                    <td>{{ trade.get("entry", "") }}</td>
                    <td>{{ trade.get("stop", "") }}</td>
                    <td>{{ trade.get("target", "") }}</td>
                    <td>{{ trade.get("grade", "") }}</td>
                    <td>{{ trade.get("confidence", "") }}%</td>
                    <td class="open">{{ trade.get("status", "") }}</td>
              </tr>
              {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="empty">
            No trades have been logged yet.
        </div>
        {% endif %}
    </div>

</div>
</body>
</html>
"""
def get_live_prices():
    symbols = ["SPY", "QQQ", "AAPL", "TSLA", "IONQ", "MU"]
    prices = {}

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d", interval="1d")

            if not data.empty:
                prices[symbol] = round(float(data["Close"].iloc[-1]), 2)
            else:
                prices[symbol] = "Unavailable"

        except Exception:
            prices[symbol] = "Unavailable"
            
    print(prices, flush=True)
    return prices
    
@app.route("/")
def dashboard():
    live_prices = get_live_prices()
    spy_price = live_prices.get("SPY")
    qqq_price = live_prices.get("QQQ")

    if isinstance(spy_price, (int, float)) and isinstance(qqq_price, (int, float)):
        market_bias = "BULLISH"
        bias_score = 2

        if spy_price > 750 and qqq_price > 710:
            market_bias = "STRONG BULLISH"
            bias_score = 3
    else:
        market_bias = "UNAVAILABLE"
        bias_score = 0
            
    trades = load_trades()
    recent_trades = list(reversed(trades[-20:]))

    total_trades = len(trades)
    open_trades = sum(
        1 for trade in trades
        if trade.get("status", "").upper() == "OPEN"
    )

    latest_trade = trades[-1] if trades else {}

    latest_signal = latest_trade.get("signal", "NO TRADE")
    latest_entry = latest_trade.get("entry", "--")
    latest_stop = latest_trade.get("stop", "--")
    latest_target = latest_trade.get("target", "--")
    latest_confidence = latest_trade.get("confidence", "--")

    return render_template_string(
        DASHBOARD_HTML,
        trades=recent_trades,
        total_trades=total_trades,
        open_trades=open_trades,
        latest_ticker=latest_trade.get("ticker", "--"),
        latest_grade=latest_trade.get("grade", "--"),
        latest_signal=latest_signal,
        latest_entry=latest_entry,
        latest_stop=latest_stop,
        latest_target=latest_target,
        latest_confidence=latest_confidence,
        live_prices=live_prices,
        market_bias=market_bias,
        bias_score=bias_score,
    )

if __name__ == "__main__":
    bot_thread = threading.Thread(
        target=start_shy_bot,
        daemon=True,
    )
    bot_thread.start()

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        use_reloader=False,
    )
