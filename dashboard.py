def show_dashboard(prices, market_bias, bias_score, confidence, trade_grade, setup_score, trade_direction, top_ticker, top_price, best_call, best_put):
    print("\n" + "="*55)
    print(" SHY AI MARKET DASHBOARD")
    print("="*55)
    
    print(f"Market Bias : {market_bias}")
    print(f"Bias Score : {bias_score}")
    print(f"Confidence : {confidence}%")
    print(f"Trade Grade : {trade_grade}")
    print(f"Setup Score : {setup_score}/5")
    print(f"Direction : {trade_direction}")
    
    print("\n" + "-"*55)
    print("WATCHLIST")
    print("-"*55)

    for ticker, price in prices.items():
        print(f"{ticker:<8} ${price:>8.2f}")

        print("\n" + "-"*55)
        print("TOP PICK")
        print("-"*55)
        print(f"Ticker : {top_ticker}")
        print(f"Price : ${top_price:.2f}")
        
        print("\n" + "-"*55)
        print("LEADERBOARD")
        print("-"*55)
        print(f"Best CALL : {best_call}")
        print(f"Best PUT : {best_put}")
    
        print("\n" + "="*55)
