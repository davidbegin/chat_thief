from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.models.user import User
from chat_thief.models.command import Command

app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def home():
    users = User.by_cool_points()
    commands = Command.by_cost()

    return render_template("beginworld_finance.html", users=users, commands=commands,)


@app.route("/user/<username>")
def profile(username):
    user = User(username)
    commands = user.commands()
    stats = user.stats()
    print(f"{user=}")
    print(f"{commands=}")
    print(f"{stats=}")
    return render_template("user.html", user=user, stats=stats, commands=commands)


@app.route("/command/<command_name>")
def command_stats(command_name):
    command = Command(command_name)
    return render_template("command.html", command=command)
