from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    resp = requests.get("http://back-app.mlakewood.svc.cluster.local:8081/message")
    if resp.status_code == 200:
        return f"<p>{resp.json()['Message']}</p>"
    else:
        return "<p>oops something bad happend</p>"