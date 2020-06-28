from pathlib import Path
import random

import requests
from tinydb import Query

from chat_thief.models.user import User
from chat_thief.models.user_code import UserCode
from chat_thief.routers.base_router import BaseRouter


BASE_URL = "https://mygeoangelfirespace.city"


class UserCodeRouter(BaseRouter):
    def route(self):
        if self.command == "css":
            return self.set_css()

        if self.command == "js":
            return self.set_js()

        if self.command == "approvejs" and self.user == "beginbotbot":
            return self.approve_js()

    def approve_js(self):
        user_to_approve = self.parser.target_user

        if user_to_approve:
            result = UserCode.db().get(Query().user == user_to_approve)
            UserCode.set_value_by_id(result.doc_id, "approved", True)
            return f"@{user_to_approve}'s JS has been approved!"
        else:
            pass

    def set_js(self):
        custom_js = self.args[0]

        UserCode(user=self.user, code_link=custom_js, code_type="js").save()

        # Switch to NOT USE requests
        response = requests.get(custom_js)

        new_js_dir = Path(__file__).parent.parent.joinpath(f"js/{self.user}")
        new_js_dir.mkdir(exist_ok=True)
        new_js_path = new_js_dir.joinpath(f"{self.user}.js")
        print(f"Saving Custom js for @{self.user} {new_js_path}")

        with open(new_js_path, "w") as f:
            f.write(response.text)

        return f"Thanks for the custom JS @{self.user}!"
        # return f"Thanks for the custom JS @{self.user}! {BASE_URL}/{self.user}.html"

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
