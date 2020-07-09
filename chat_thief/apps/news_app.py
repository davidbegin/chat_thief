from dataclasses import dataclass
from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.economist.facts import Facts
from chat_thief.models.user import User


app = Flask(__name__, template_folder="../templates")


@app.route("/")
def facts(name=None):
    while True:
        facts = Facts()
        breaking_news = facts.breaking_news()

        stats = None
        if "user" in breaking_news:
            if breaking_news["user"]:
                user = User(breaking_news["user"])
                stats = user.stats()

        if breaking_news:
            # this needs a specific template
            category = breaking_news.get("category", None)
            revolutionaries = breaking_news.get("revolutionaries", None)
            peace_keepers = breaking_news.get("peace_keepers", None)
            fence_sitters = breaking_news.get("fence_sitters", None)

            if category in ["peace", "revolution", "coup"]:
                print("Rendering A Coup")
                return render_template(
                    "news.html",
                    category=category,
                    stats=stats,
                    scope=breaking_news["scope"],
                    revolutionaries=revolutionaries,
                    peace_keepers=peace_keepers,
                    fence_sitters=fence_sitters,
                )
            elif category == "iasip":
                return render_template("sunny.html", title_card=breaking_news["scope"])
            else:
                print("Rendering The News")
                return render_template(
                    "news.html",
                    category=category,
                    stats=stats,
                    scope=breaking_news["scope"],
                )
        else:
            time.sleep(1)


if __name__ == "news_app":
    app.run(debug=True)
