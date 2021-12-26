import os
import flask
import threading
import hashlib
import logger

app = flask.Flask("")
mime: str = "application/json"


def slog(data: str):
  logger.log("log", data, os.environ["log"])


def status(info: str) -> str:
  return "{'status':'" + info + "'}"


@app.route("/log", methods=["POST"])
def log():
  received = flask.request.json
  
  for c in ["cat", "data", "token"]:
    if(not c in received):
      slog(f"Log invaild post: field '{c}' is missing")
      return flask.Response(status("Invaild post"), status=400, mimetype=mime)

  cat: str = received["cat"]
  data: str = received["data"]
  token: str = received["token"]
  
  if(logger.log(cat, data, token)):
    slog(f"Log successed: {cat}")
    return flask.Response(status("Successed"), status=200, mimetype=mime)
  else:
    slog(f"Log invaild token '{token}' for '{cat}'")
    return flask.Response(status("Invaild token"), status=401, mimetype=mime)


@app.route("/login", methods = ["POST", "GET"])
def login():
  if(flask.request.method == "POST"):
    token = flask.request.form["token"]

    if(token != ""):
      resp = flask.make_response(flask.redirect("/view"))
      sha: str = hashlib.sha256(token.encode()).hexdigest()
      resp.set_cookie("token", sha)
      return resp
  
  else:
    token: str = flask.request.cookies.get("token")

    if(token == os.environ["login_token"]):
      return flask.redirect("/view")

    return flask.render_template("login.html")


@app.route("/view")
def view_root():
  token: str = flask.request.cookies.get("token")
  
  if(token == ""):
    return flask.redirect("/login")
    
  elif(token != os.environ["login_token"]):
    slog(f"Invaild login token: {token}")
    return flask.redirect("/login?try-again=1") 

  slog("Successfully logged in")
  return flask.redirect("/view/log")


@app.route("/view/<cat>")
def view(cat):
  token: str = flask.request.cookies.get("token")
  
  if(token == ""):
    return flask.redirect("/login")
    
  elif(token != os.environ["login_token"]):
    slog(f"Invaild view token: {token}")
    return flask.redirect("/login?try-again=1")
    
  if(os.path.exists(f"logs/{cat}.log")):
    slog(f"Viewed log: {cat}")
    return logger.view_html_reversed(cat)
      
  else:
    return f"{cat} does not exists"


@app.route("/")
def root():
  return login()


def run():
  app.run(host = '0.0.0.0', port = 8080)

def alive():
  t = threading.Thread(target = run)
  t.start()