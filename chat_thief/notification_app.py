from typing import Dict, List
import time

from flask import Flask
from flask import render_template

from chat_thief.models.notification import Notification


app = Flask(__name__)
app.run(debug=True)


@app.route("/")
def facts(name=None):
    last_notification = Notification.last()
    return render_template(
        "notification.html", notifications=[last_notification["message"]]
    )
