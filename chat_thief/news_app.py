from dataclasses import dataclass
from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.economist.facts import Facts
from chat_thief.models.user import User


app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def facts(name=None):
    while True:
        facts = Facts()
        breaking_news = facts.breaking_news()

        stats = None
        if "user" in breaking_news:
            user = User(breaking_news["user"])
            stats = user.stats()

        return render_template("news.html", stats=stats, scope=breaking_news["scope"])
        time.sleep(1)
