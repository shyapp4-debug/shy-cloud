import yfinance as yf
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
EMAIL_ADDRESS = "shyapp4@gmail.com"
EMAIL_PASSWORD = "cyfr uujx leei jarn"
SEND_TO = "cecilshy8@yahoo.com"
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = SEND_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, SEND_TO, msg.as_string())
    server.quit()
last_signal = None
last_target = None
last_stop = None
signal = "NO TRADE"
setup_score = 0
trade_grade = "N/A"
entry = 0
stop = 0
target_price = 0
risk_reward = 0
trade_count = 0
max_trades = 3
while True:
    
    print("checking market...")

    if trade_count >= max_trades:
        print("DAILY TRADE LIMIT REACHED")
        time.sleep(300)
        continue

    with open("watchlist.txt", "r") as f:
        symbols = [line.strip() for line in f if line.strip()]
    prices = {}

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.fast_info["last_price"]
            display_symbol = "SPX" if symbol == "^GSPC" else "BRK.B" if symbol == "BRK-B" else symbol
            prices[display_symbol] = round(price, 2)
            time.sleep(5)
        except Exception as e:
            display_symbol = "SPX" if symbol == "^GSPC" else "BRK.B" if symbol == "BRK-B" else symbol
            prices[display_symbol] = 0
    print(f"{display_symbol}: unavailable")

    print("\n----- SHY MARKET DASHBOARD -----")

    for ticker, price in prices.items():
        print(f"{ticker}: {price}")

    bias_score = 0

    if prices["QQQ"] > 730:
        bias_score += 1
    else:
        bias_score -= 1

    if prices["SPY"] > 750:
        bias_score += 1
    else:
        bias_score -= 1

    if prices["SPX"] > 7000:
        bias_score += 1
    else:
        bias_score -= 1

    if bias_score == 3:
        market_bias = "STRONG BULLISH"
    elif bias_score == 2:
        market_bias = "BULLISH"
    elif bias_score == -3:
        market_bias = "STRONG BEARISH"
    elif bias_score == -2:
        market_bias = "BEARISH"
    else:
        market_bias = "NEUTRAL / WAIT"

    print(f"Market Bias Score: {bias_score}")
    print("Market Bias:", market_bias)

    setup_score = 0
    trade_grade = "NO TRADE"
    trade_direction = "WAIT"

    if market_bias == "STRONG BULLISH":
        setup_score = 5
        trade_grade = "A+"
        trade_direction = "CALL"
    elif market_bias == "BULLISH":
        setup_score = 4
        trade_grade = "A"
        trade_direction = "CALL"
    elif market_bias == "STRONG BEARISH":
        setup_score = 5
        trade_grade = "A+"
        trade_direction = "PUT"
    elif market_bias == "BEARISH":
        setup_score = 4
        trade_grade = "A"
        trade_direction = "PUT"
    else:
        setup_score = 1
        trade_grade = "NO TRADE"
        trade_direction = "WAIT"

    print(f"Setup Score: {setup_score}/5")
    print(f"Trade Grade: {trade_grade}")
    print("\n----- SHY WATCHLIST SCANNER -----")

    top_ticker = None
    top_price = 0

    for symbol in symbols:
        if symbol in prices:
            if prices[symbol] > top_price:
                top_price = prices[symbol]
                top_ticker = symbol

    print(f"Top Ticker: {top_ticker}")
    print(f"Top Price: {top_price}")
    print(f"Trade Direction: {trade_direction}")
    print("\n----- SHY LEADERBOARD -----")
    
    best_call = None
    best_put = None

    for symbol in symbols:
        if symbol in prices:

            if best_call is None or prices[symbol] > prices.get(best_call, 0):
                best_call = symbol

            if best_put is None or prices[symbol] < prices.get(best_put, 999999):
                best_put = symbol

    print(f"Best Call Candidate: {best_call}")
    print(f"Best Put Candidate: {best_put}")
    sorted_prices = sorted(
        prices.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for i, (ticker, price) in enumerate(sorted_prices[:5], start=1):
        print(f"#{i} {ticker}: {price}")
    if market_bias == "NEUTRAL / WAIT":
        print("NO TRADE - MARKET BIAS NOT STRONG ENOUGH")

    with open("shy_trades.txt", "a") as log:
        log.write(f"{datetime.now()} | {market_bias} | Score: {bias_score} | QQQ: {prices['QQQ']} | SPY: {prices['SPY']}\n")

        print("\n----- SHY SIGNALS -----")
    if prices["QQQ"] > 725 and prices["SPY"] > 750:
        print("🚀 QQQ BREAKOUT")
        setup_score = 4
        trade_grade = "A"
        entry = 725
        stop = 723
        target_price = 728
        risk = entry - stop
        reward = target_price - entry
        risk_reward = round(reward / risk, 2)
        print(f"Setup Score: {setup_score}/5")
        print(f"Trade Grade: {trade_grade}")
        print(f"Entry: {entry}")
        print(f"Stop: {stop}")
        print(f"Target: {target_price}")
        print(f"Risk/Reward: 1:{risk_reward}")
        print("CALLS FAVORABLE")
        signal = "QQQ BREAKOUT"

    if signal != last_signal and trade_grade in ["A+", "A"]:
        with open("shy_trades.txt", "a") as log:
            log.write(f"{datetime.now()}\n")
            log.write(f"{signal}\n")
            log.write(f"QQQ: {prices['QQQ']}\n")
            log.write(f"SPY: {prices['SPY']}\n")
            log.write(f"Grade: {trade_grade}\n")
            log.write(f"Entry: {entry}\n")
            log.write(f"Stop: {stop}\n")
            log.write(f"Target: {target_price}\n")
            log.write(f"RiskReward: 1:{risk_reward}\n")
            log.write("-----------------\n")
        send_email(
            "SHY CALL ALERT",
            f"""
    Ticker: QQQ
Signal: {signal}
Direction: {trade_direction}

Entry: {entry}
Stop: {stop}
Target: {target_price}
Risk/Reward: 1:{risk_reward}

Market Bias: {market_bias}
Setup Score: {setup_score}/5
Trade Grade: {trade_grade}

Action: WATCH {trade_direction}
    TSLA: {prices['TSLA']}
    IONQ: {prices['IONQ']}
    QBTS: {prices['QBTS']}
    TQQQ: {prices['TQQQ']}
    """
        )
        last_signal = signal

        target = "QQQ TARGET HIT"

        if prices["QQQ"] > 728 and target != last_target:
            send_email(
                "SHY TARGET ALERT",
                f"""
        Target Hit: QQQ above 728

        QQQ: {prices['QQQ']}
        SPY: {prices['SPY']}

        Action: TAKE PROFIT / REVIEW TRADE
        """
            )
            last_target = target
    stop_signal = "QQQ STOP HIT"

    if prices["QQQ"] < 723 and stop_signal != last_stop:
        send_email(
            "SHY STOP ALERT",
            f"""
    Stop Hit: QQQ below 723

    QQQ: {prices['QQQ']}
    SPY: {prices['SPY']}

    Action: EXIT TRADE / PROTECT CAPITAL
    """
        )
        last_stop = stop_signal

    if prices["QQQ"] < 720 and prices["SPY"] < 740:
        print("🔻 QQQ BREAKDOWN")
        print("PUTS FAVORABLE")
        signal = "QQQ BREAKDOWN"

        if signal != last_signal:
            with open("shy_trades.txt", "a") as log:
                log.write(f"{datetime.now()}\n")
                log.write(f"{signal}\n")
                log.write(f"QQQ: {prices['QQQ']}\n")
                log.write(f"SPY: {prices['SPY']}\n")
                log.write("-----------------\n")

            send_email(
                "SHY PUT ALERT",
                f"""
    Signal: {signal}

    QQQ: {prices['QQQ']}
    Market Bias: {market_bias}

    Action: WATCH PUTS

    TSLA: {prices['TSLA']}
    IONQ: {prices['IONQ']}
    QBTS: {prices['QBTS']}
    TQQQ: {prices['TQQQ']}
    """
        )
        else:
            pass
    if market_bias == "BULLISH / CALLS FAVORABLE":
        print("QQQ: WATCH CALLS")
        print("SPY: WATCH CALLS")
        print("TSLA: WATCH CALLS")
        print("MU: WATCH CALLS")
        print("TQQQ: WATCH CALLS")

    elif market_bias == "BEARISH / PUTS FAVORABLE":
        print("QQQ: WATCH PUTS")
        print("SPY: WATCH PUTS")
        print("TSLA: WATCH PUTS")
        print("MU: WATCH PUTS")
        print("TQQQ: WATCH PUTS")
    print("\n----- TOP WATCHLIST -----")

    watchlist = ["TSLA", "IONQ", "QBTS", "TQQQ"]

    for stock in watchlist:
        try:
            price = yf.Ticker(stock).info["regularMarketPrice"]
            print(f"{stock}: {price}")
        except:
            print(f"{stock}: unavailable")

    time.sleep(300)
    



