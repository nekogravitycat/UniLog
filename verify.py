import os

def check(cat: str, token: str) -> bool:
  if(cat in os.environ):
    return token == os.environ[cat]
  else:
    return False