from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.models.notification import Notification


app = Flask(__name__, template_folder="../templates")


@app.route("/")
def facts(name=None):
    last_notification = Notification.last()
    if last_notification:
        message = last_notification["message"]
        duration = last_notification["duration"]
    else:
        message = None
        duration = None

    return render_template(
        "notification.html", notification=message, refresh_time=duration
    )


if __name__ == "notification_app":
    app.run(debug=True)
