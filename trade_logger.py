import csv
import os
from datetime import datetime

TRADE_LOG_FILE = "shy_trade_log.csv"

def log_trade(
    ticker,
    direction,
    signal,
    entry,
    stop,
    target,
    grade,
    confidence,
):
  file_exists = os.path.exists(TRADE_LOG_FILE)

  with open(TRADE_LOG_FILE, "a", newline="") as file:
      writer = csv.writer(file)

      if not file_exists:
          writer.writerow([
              "timestamp",
              "ticker",
              "direction",
              "signal",
              "entry",
              "stop",
              "target",
              "grade",
              "confidence",
              "status",
          ])

      writer.writerow([
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          ticker,
          direction,
          signal,
          entry,
          stop,
          target,
          grade,
          confidence,
          "OPEN",
      ])

  print("TRADE SAVED TO SHY JOURNAL")
if __name__ == "__main__":
    log_trade(
        "QQQ",
        "CALL",
        "TEST BREAKOUT",
        721.34,
        719.00,
        725.00,
        "A",
        90,
    )
