from pathlib import Path
import random

import requests

from chat_thief.models.user import User
from chat_thief.routers.base_router import BaseRouter


BASE_URL = "https://mygeoangelfirespace.city"


class UserCodeRouter(BaseRouter):
    def route(self):
        if self.command == "css":
            # if self.user in STREAM_LORDS:
            return self.set_css()

    def set_css(self):
        custom_css = self.args[0]
        User(self.user).set_value("custom_css", custom_css)

        # Switch to NOT USE requests
        response = requests.get(custom_css)
        new_css_path = Path(__file__).parent.parent.joinpath(f"static/{self.user}.css")
        print(f"Saving Custom CSS for @{self.user} {new_css_path}")
        with open(new_css_path, "w") as f:
            f.write(response.text)

        return f"Thanks for the custom CSS @{self.user}! {BASE_URL}/{self.user}.html"
