from flask import Flask

app = Flask(__name__)


@app.route("/message")
def hello_world():
    return {"Message": "Hello, World!"}