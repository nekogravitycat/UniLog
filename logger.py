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
  with open(f"logs/{cat}.log", "a+") as f:
    f.write(f"[{now}] {data}\n")
    
  if(cat == "log"):
    print(data)
    
  return True


def view_html_reversed(cat: str) -> str:
  with open(f"logs/{cat}.log") as f:
    result = ""
    for l in reversed(f.readlines()):
      result += l + "<br>"
    return result