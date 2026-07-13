from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    if os.path.exists("shy_trade_log.csv"):
        df = pd.read_csv("shy_trade_log.csv")
        table = df.tail(20).to_html(index=False)
    else:
        table = "<h3>No trades yet.</h3>"

    return f"""
    <html>
    <head>
        <title>SHY Dashboard</title>
        <style>
            body {{
                background:#111;
                color:white;
                font-family:Arial;
                padding:30px;
            }}
            h1 {{
                color:#00ff66;
            }}
            table {{
                border-collapse:collapse;
                width:100%;
                background:white;
                color:black;
            }}
            th,td {{
                border:1px solid #ccc;
                padding:8px;
                text-align:center;
            }}
        </style>
    </head>

    <body>
        <h1>SHY LIVE DASHBOARD</h1>

        <h2>Latest Trades</h2>

        {table}

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
