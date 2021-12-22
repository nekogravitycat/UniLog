from datetime import datetime, timezone, timedelta

def log(cat: str, data: str):
  now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
  f = open(f"logs/{cat}.log", "a")
  f.write(f"[{now}] {data}\n")
  f.close()