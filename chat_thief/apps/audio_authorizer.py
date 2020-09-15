from flask import Flask
from flask import render_template

from chat_thief.models.user import User
from chat_thief.models.command import Command

app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():
    users = User.by_cool_points()
    commands = Command.by_cost()
    return render_template("beginworld_finance.html", users=users, commands=commands,)


@app.route("/sound/<sound>/allowed/<username>")
def profile(sound, username):
    user = User(username)
    allowed = Command(sound).allowed_to_play(username)
    return {"allowed": allowed}
    # return render_template("user.html", user=user, stats=stats, commands=commands)


# @app.route("/command/<command_name>")
# def command_stats(command_name):
#     command = Command(command_name)
#     sfx_vote = SFXVote(command_name)
#     return render_template(
#         "command.html",
#         command=command,
#         like_to_hate_ratio=sfx_vote.like_to_hate_ratio(),
#     )


if __name__ == "audio_authorizer":
    app.run(debug=True)
