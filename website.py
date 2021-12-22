import flask
import threading
import logger
import verify

app = flask.Flask("")
mime: str = "application/json"


def status(info: str) -> str:
  return "{'status':'" + info + "'}"


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
      return flask.Response(status("Invaild post"), status=400, mimetype=mime)

  cat: str = received["cat"]
  data: str = received["data"]
  token: str = received["token"]
  
  if(logger.log(cat, data, token)):
    return flask.Response(status("Successed"), status=200, mimetype=mime)
  else:
    return flask.Response(status("Invaild token"), status=401, mimetype=mime)


def run():
  app.run(host = '0.0.0.0', port = 8080)

def alive():
  t = threading.Thread(target = run)
  t.start()