from pathlib import Path

import requests

from chat_thief.models.user import User
from chat_thief.models.user_code import UserCode
from chat_thief.models.user_page import UserPage
from chat_thief.routers.base_router import BaseRouter
from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser


BASE_URL = "https://mygeoangelfirespace.city"


class UserCodeRouter(BaseRouter):
    def route(self):
        self.url_parser = SoundeffectRequestParser(self.user, self.args).parse()

        if self.command == "css":
            return self.set_css()

        if self.command == "js":
            return self.set_js()

        if self.command == "approvejs" and self.user in STREAM_LORDS:
            return self.approve_js()

        if self.command == "buyjs":
            return self.buy_js()

        if self.command == "deactivate" or self.command == "removejs":
            js_to_deactivate = self.args[0]
            UserPage.deactivate(self.user, js_to_deactivate)
            return f"Attempting to remove: {js_to_deactivate}"

        if self.command == "activate" or self.command == "addjs":
            js_to_add = self.args[0]
            UserPage.activate(self.user, js_to_add)
            return f"Attempting to Reactivate: {js_to_add}"

    # What does JS COST?
    # Should we let developers decide???
    # For Now its free, and theres a Widget Leaderboard
    def buy_js(self):
        # user_to_approve = self.parser.target_user
        potential_widget = self.args[0]
        return UserCode.purchase(self.user, potential_widget)

    def approve_js(self):
        user_to_approve = self.parser.target_user
        potential_widget = self.args[0]
        print(f"Attempting to Approve Potential Widget: {potential_widget}")
        return UserCode.approve(user_to_approve, potential_widget)

    def set_js(self):
        custom_js = self.url_parser.youtube_id
        name = self.url_parser.command

        user_code = UserCode(
            user=self.user, code_link=custom_js, code_type="js", name=name
        ).update_or_create()

        # Switch to NOT USE requests
        response = requests.get(custom_js)

        new_js_dir = Path(__file__).parent.parent.joinpath(f"js")
        new_js_dir.mkdir(exist_ok=True)

        new_js_path = new_js_dir.joinpath(f"{user_code._name}.js")
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
