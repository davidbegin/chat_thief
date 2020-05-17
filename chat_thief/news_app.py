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

        # richest_user
        # coup
        # richest_command
        # We need an event type
        stats = None
        # if "user" in breaking_news:
        #     if breaking_news["user"]:
        #         user = User(breaking_news["user"])
        #         stats = user.stats()

        # this needs a specific template
        category = breaking_news.get("category", None)
        revolutionaries = breaking_news.get("revolutionaries", None)
        peace_keepers = breaking_news.get("peace_keepers", None)
        fence_sitters = breaking_news.get("fence_sitters", None)

        # What do we really want?

        return render_template(
            "coup.html",
            category=category,
            stats=stats,
            scope=breaking_news["scope"],
            revolutionaries=revolutionaries,
            peace_keepers=peace_keepers,
            fence_sitters=fence_sitters,
        )
        time.sleep(1)
