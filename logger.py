import os
from datetime import datetime, timezone, timedelta


def check(cat: str, token: str) -> bool:
  if(cat in os.environ):
    return token == os.environ[cat]
  else:
    return False


def log(cat: str, data: str, token: str) -> bool:
  if(not check(cat, token)):
    return False
  now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
  f = open(f"logs/{cat}.log", "a")
  f.write(f"[{now}] {data}\n")
  f.close()
  return True