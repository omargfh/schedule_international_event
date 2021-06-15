import json5

from flask import Flask, flash, redirect, render_template, request, session

from models.input import user_input
from models.console import input_to_graphs

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Disable cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        print(request.form.get("js_obj"))
    return render_template("index.html")

@app.route('/results')
def results():
    return render_template("results.html")