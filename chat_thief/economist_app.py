from dataclasses import dataclass
from typing import Dict, List
import time

from flask import Flask
from flask import render_template


from chat_thief.economist.facts import Facts


@dataclass
class FactsView:
    available_sounds: int
    unavailable_sounds: int
    cool_points: int
    street_cred: int
    top_users: List


app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def facts(name=None):
    while True:
        facts = Facts()

        facts_view = FactsView(
            available_sounds=facts.available_sounds(),
            unavailable_sounds=facts.unavailable_sounds(),
            cool_points=facts.cool_points(),
            top_users=facts.top_users(),
            street_cred=facts.street_cred(),
        )

        return render_template("index.html", facts=facts_view)
        time.sleep(1)
