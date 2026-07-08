def get_signal(market_bias, prices):
    signal = "NO TRADE"
    trade_direction = "WAIT"
    setup_score = 1
    trade_grade = "NO TRADE"

    if market_bias == "STRONG BULLISH":
        signal = "QQQ BREAKOUT"
        trade_direction = "CALL"
        setup_score = 5
        trade_grade = "A+"

    elif market_bias == "STRONG BEARISH":
        signal = "QQQ BREAKDOWN"
        trade_direction = "PUT"
        setup_score = 5
        trade_grade = "A+"

    return {
        "signal": signal,
        "direction": trade_direction,
        "setup_score": setup_score,
        "trade_grade": trade_grade
    }
