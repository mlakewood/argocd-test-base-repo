from flask import Flask
import requests
import environ
import structlog

logger = structlog.get_logger()
app = Flask(__name__)

@environ.config
class AppConfig:
    back_app_host = environ.var(help="This is the back_app hostname")
    back_app_port = environ.var(help="This is the back_app port")


@app.route("/health")
def health():
    return "ok"

@app.route("/")
def hello_world():
    cfg = environ.to_config(AppConfig)

    resp = requests.get(f"http://{cfg.back_app_host}:{cfg.back_app_port}/message")
    if resp.status_code == 200:
        return f"<p>{resp.json()['Message']}</p>"
    else:
        return "<p>oops something bad happend</p>"