from pathlib import Path
import random

import requests

from chat_thief.models.user import User
from chat_thief.routers.base_router import BaseRouter


BASE_URL = "https://mygeoangelfirespace.city"


class UserCodeRouter(BaseRouter):
    def route(self):
        if self.command == "css":
            return self.set_css()

        if self.command == "js":
            return self.set_js()

    def set_js(self):
        custom_js = self.args[0]
        # We Might want to create Widgets
        # User(self.user).set_value("custom_js", custom_js)

        # Switch to NOT USE requests
        response = requests.get(custom_js)
        # We need a JS Path
        new_js_path = Path(__file__).parent.parent.joinpath(f"static/{self.user}.js")
        print(f"Saving Custom js for @{self.user} {new_js_path}")
        with open(new_js_path, "w") as f:
            f.write(response.text)

        return f"Thanks for the custom JS @{self.user}! {BASE_URL}/{self.user}.html"

    # UserCode("user", "url", "lang")
    def set_css(self):
        custom_css = self.args[0]
        # We Might want to create Widgets
        User(self.user).set_value("custom_css", custom_css)

        # Switch to NOT USE requests
        response = requests.get(custom_css)
        new_css_path = Path(__file__).parent.parent.joinpath(f"static/{self.user}.css")
        print(f"Saving Custom CSS for @{self.user} {new_css_path}")
        with open(new_css_path, "w") as f:
            f.write(response.text)

        return f"Thanks for the custom CSS @{self.user}! {BASE_URL}/{self.user}.html"
