from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.models.user import User
from chat_thief.models.command import Command

app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def index():
    users = User.by_cool_points()
    commands = Command.by_cost()

    return render_template("beginworld_finance.html", users=users, commands=commands)


@app.route("/user/<username>")
def user(username):
    user = User(user)
    commands = user.commands()
    stats = user.stats()

    return render_template("user.html", stats=stats, commands=commands)
