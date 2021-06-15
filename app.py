import json5
import random


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
        user_input = json5.loads(request.form.get("js_obj"))
        print(user_input)
        id = str(random.randint(0, 10000000))
        input_to_graphs(user_input, id)
        return redirect(f"/results?id={id}")
    return render_template("index.html")

@app.route('/results')
def results():
    id = request.args.get("id")
    print(type(request.args.get("saveNew")))
    saveNew = "false" if request.args.get("saveNew") == "false" else "true"
    return render_template("results.html", id=id, saveNew=saveNew)