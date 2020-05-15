from dataclasses import dataclass
from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.economist.facts import Facts


app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def facts(name=None):
    while True:
        facts = Facts()
        return render_template("news.html", facts=facts)
        time.sleep(1)
