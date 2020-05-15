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

        category = None
        if "category" in breaking_news:
            category = breaking_news["category"]

        stats = None
        if "user" in breaking_news:
            user = User(breaking_news["user"])
            stats = user.stats()

        return render_template(
            "news.html",
            category=category,
            stats=stats,
            scope=breaking_news["scope"],
            revolutionaries=breaking_news["revolutionaries"],
            peace_keepers=breaking_news["peace_keepers"],
            fence_sitters=breaking_news["fence_sitters"],
        )
        time.sleep(1)
