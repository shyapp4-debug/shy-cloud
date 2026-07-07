def get_market_bias(prices):
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
