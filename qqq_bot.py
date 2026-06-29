import yfinance as yf
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
EMAIL_ADDRESS = "shyapp4@gmail.com"
EMAIL_PASSWORD = "vtbv mnpj jzgg ctqy"
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
    ema20 = {}
    ema50 = {}

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.fast_info["last_price"]
            display_symbol = "SPX" if symbol == "^GSPC" else "BRK.B" if symbol == "BRK-B" else symbol
            prices[display_symbol] = round(price, 2)
            hist = ticker.history(period="5d", interval="5m")
            ema20[display_symbol] = round(hist["Close"].ewm(span=20).mean().iloc[-1], 2)
            ema50[display_symbol] = round(hist["Close"].ewm(span=50).mean().iloc[-1], 2)
            time.sleep(5)
        except Exception as e:
            display_symbol = "SPX" if symbol == "^GSPC" else "BRK.B" if symbol == "BRK-B" else symbol
            prices[display_symbol] = 0
    print(f"SHY{display_symbol}: unavailable")

    print("\n----- SHY MARKET DASHBOARD -----")

    for ticker, price in prices.items():
        print(f"SHY{ticker}: {price}")

    bias_score = 0

    if prices.get("QQQ", 0) > prices.get("SPY", 0) * 0.96:
        bias_score += 1
    else:
        bias_score -= 1

    if prices.get("QQQ", 0) > 700:
        bias_score += 1
    else:
        bias_score -= 1

    if prices.get("SPY", 0) > 725:
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

    print(f"SHYMarket Bias Score: {bias_score}")
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

    print(f"SHYSetup Score: {setup_score}/5")
    print(f"SHYTrade Grade: {trade_grade}")
    confidence = 0

    if market_bias == "STRONG BULLISH":
        confidence += 25

    if setup_score == 5:
        confidence += 25

    if trade_grade == "A+":
        confidence += 25

    if trade_direction != "WAIT":
        confidence += 25

    print(f"SHYConfidence: {confidence}%")
    print(f"SHYMarket Bias Score: {bias_score}")
    print(f"SHYMarket Bias: {market_bias}")
    
    print("\n----- SHY WATCHLIST SCANNER -----")

    top_ticker = None
    top_price = 0

    for symbol in symbols:
        if symbol in prices:
            if prices[symbol] > top_price:
                top_price = prices[symbol]
                top_ticker = symbol

    print(f"SHYTop Ticker: {top_ticker}")
    print(f"SHYTop Price: {top_price}")
    print(f"SHYTrade Direction: {trade_direction}")
    print("\n----- SHY LEADERBOARD -----")
    
    best_call = None
    best_put = None

    for symbol in symbols:
        if symbol in prices:

            if best_call is None or prices[symbol] > prices.get(best_call, 0):
                best_call = symbol

            if best_put is None or prices[symbol] < prices.get(best_put, 999999):
                best_put = symbol

    print(f"SHYBest Call Candidate: {best_call}")
    print(f"SHYBest Put Candidate: {best_put}")
    current_alert = f"SHY{best_call}-{best_put}-{market_bias}-{trade_grade}"

    try:
        with open("last_alert.txt", "r") as f:
            last_alert = f.read().strip()
    except:
        last_alert = ""

    if current_alert != last_alert:
        send_email(
            "SHY WATCHLIST ALERT",
            f"SHY {top_ticker} CALL ALERT",
    Best Call Candidate: {best_call}

    Best Put Candidate: {best_put}

    Market Bias: {market_bias}
    Trade Grade: {trade_grade}

    Action: WATCH
    """
        )

        with open("last_alert.txt", "w") as f:
            f.write(current_alert)
            print("WATCHLIST EMAIL SENT")
            print("CONTINUING TO SIGNALS...")
    sorted_prices = sorted(
        prices.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for i, (ticker, price) in enumerate(sorted_prices[:5], start=1):
        print(f"SHY#{i} {ticker}: {price}")
        
    if market_bias == "NEUTRAL / WAIT":
        print("NO TRADE - MARKET BIAS NOT STRONG ENOUGH")
    
        with open("shy_trades.txt", "a") as log:
            og.write(f"SHY{datetime.now()} | {market_bias} | Score: {bias_score} | QQQ: {prices.get('QQQ', 0)} | SPY: {prices.get('SPY', 0)}\n")
    
    print("\n----- SHY SIGNALS -----")
    if (
        market_bias == "STRONG BEARISH"
        and best_put is not None
        and prices.get(best_put, 0) > 0
    ):

        print("🔻 QQQ BREAKDOWN")
        setup_score = 5
        trade_grade = "A+"
        entry = prices.get("QQQ", 0)
        stop = entry + 2
        target_price = entry - 4
        risk_reward = 2.0
        trade_direction = "PUT"
        signal = "QQQ BREAKDOWN"
    if (
        market_bias == "STRONG BULLISH"
        and prices.get("QQQ", 0) > 725
        and prices("SPY", 0) > 728
    ):
        print("🚀 QQQ BREAKOUT")
        ...
        signal =("QQQ BREAKOUT")
        if best_call is None:
            print("NO VALID CALL CANDIDATE - SKIPPED CALL EMAIL")
            continue
        signal = "QQQ BREAKOUT"

    elif (
        market_bias == "STRONG BEARISH"
        and prices.get("QQQ", 0) < 720
    ):
        print("🔻 QQQ BREAKDOWN")
        
        setup_score = 5
        trade_grade = "A"
        entry = prices.get("QQQ", 0)
        stop = entry - 2
        target_price = entry + 4
        risk_reward = 2.0
        trade_direction = "CALL"
        signal = "QQQ BREAKOUT"
        print(f"SHYSetup Score: {setup_score}/5")
        print(f"SHYTrade Grade: {trade_grade}")
        print(f"SHYEntry: {entry}")        
        print(f"SHYStop: {stop}")
        print(f"SHYTarget: {target_price}")
        print(f"SHYRisk/Reward: 1:{risk_reward}")
        print("CALLS FAVORABLE")
        signal = f"SHY{best_call} BREAKOUT"
    
    if signal != last_signal and trade_grade in ["A+", "A"]:
        with open("shy_trades.txt", "a") as log:
            log.write(f"SHY{datetime.now()}\n")
            log.write(f"SHY{signal}\n")
            log.write(f"SHY{best_call}: {prices.get(best_call, 0)}\n")
            log.write(f"SHYSPY: {prices.get('SPY', 0)}\n")
            log.write(f"SHYGrade: {trade_grade}\n")
            log.write(f"SHYEntry: {entry}\n")
            log.write(f"SHYStop: {stop}\n")
            log.write(f"SHYTarget: {target_price}\n")
            log.write(f"SHYRiskReward: 1:{risk_reward}\n")
            log.write("-----------------\n")
    if top_ticker is None:
        print("NO VALID CALL CANDIDATE - SKIPPING CALL EMAIL")
        continue
        print(f"SENDING {top_ticker} CALL ALERT EMAIL NOW")
        send_email(
            f"SHY {top_ticker} CALL ALERT",
            f'''
        Ticker: {top_ticker}
        Signal: {signal}
        Direction: {trade_direction}
        
        Entry: {entry}
        Stop: {stop}
        Target: {target_price}
        Risk/Reward: 1:{risk_reward}
        
        Market Bias: {market_bias}
        Setup Score: {setup_score}/5
        Trade Grade: {trade_grade}
        Confidence: {confidence}%
        
        Action: Enter {trade_direction}
        TSLA: {prices.get('TSLA', 0)}
        IONQ: {prices.get('IONQ', 0)}
        QBTS: {prices.get('QBTS', 0)}
        TQQQ: {prices.get('TQQQ', 0)}
        """
        )
        last_signal = signal
        trade_count += 1
        time.sleep (300)
                
