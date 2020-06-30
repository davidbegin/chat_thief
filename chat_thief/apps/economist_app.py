from dataclasses import dataclass
from typing import Dict, List
import time

from flask import Flask
from flask import render_template


from chat_thief.economist.facts import Facts


@dataclass
class FactsView:
    revolution_count: int
    peace_count: int
    total_votes: int
    available_sounds: int
    unavailable_sounds: int
    total_sounds: int
    cool_points: int
    street_cred: int
    top_users: List
    most_popular: List


app = Flask(__name__, template_folder="../templates")


@app.route("/")
def facts(name=None):
    while True:
        facts = Facts()

        most_popular = facts.most_popular()
        most_popular.reverse()

        facts_view = FactsView(
            total_votes=facts.total_votes(),
            available_sounds=facts.available_sounds(),
            revolution_count=facts.revolution_count(),
            peace_count=facts.peace_count(),
            unavailable_sounds=facts.unavailable_sounds(),
            total_sounds=facts.total_sounds(),
            cool_points=facts.cool_points(),
            top_users=facts.top_users(),
            street_cred=facts.street_cred(),
            most_popular=most_popular,
        )

        return render_template("index.html", facts=facts_view)
        time.sleep(1)


if __name__ == "economist_app":
    app.run(debug=True)
