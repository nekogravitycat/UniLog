import flask
import threading
import logger
import verify

app = flask.Flask("")


@app.route("/")
def root():
  return "hello world"


@app.route("/view/<data>")
def view(data):
  return f"here's the place for viewing {data}"


@app.route("/log", methods=["POST"])
def log():
  received = flask.request.json
  
  for c in ["cat", "data", "token"]:
    if(not c in received):
      return "Invaild post"
      
  cat: str = received["cat"]
  data: str = received["data"]
  token: str = received["token"]
  
  if(verify.check(cat, token)):
    logger.log(cat, data)
    return "Successed"
  else:
    return "Invaild token"


@app.route("/test/<c>/<v>")
def test(c, v):
  logger.log(c, v)
  return "done!"


def run():
  app.run(host = '0.0.0.0', port = 8080)

def alive():
  t = threading.Thread(target = run)
  t.start()