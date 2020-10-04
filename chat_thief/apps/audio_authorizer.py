from flask import Flask
from flask import render_template

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.config.stream_lords import STREAM_GODS

app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():
    users = User.by_cool_points()
    commands = Command.by_cost()
    return render_template("beginworld_finance.html", users=users, commands=commands,)


@app.route("/sound/<sound>/allowed/<username>")
def authorizer(sound, username):
    user = User(username)
    mana = user.mana()
    streamlord = username in STREAM_GODS

    owned = Command(sound).allowed_to_play(username)
    if streamlord:
        allowed = True
    else:
        allowed = owned and mana > 0

    if allowed:
        user.update_mana(-1)

    result = {"allowed": allowed, "owned": owned, "streamlord": streamlord, "extra": False, "mana": mana}

    print(f"\n\n\t{result=}")

    return result

if __name__ == "audio_authorizer":
    app.run(debug=True)
