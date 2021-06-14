from flask import Flask
from models.input import user_input
from models.console import input_to_graphs

app = Flask(__name__)


@app.route('/')
def hello():
    input_to_graphs(user_input)
    return '<img src="/static/final.png">'