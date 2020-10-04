from pathlib import Path

import pytest

from chat_thief.routers.user_code_router import UserCodeRouter
from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.user_code import UserCode
from chat_thief.models.user_page import UserPage

from tests.support.database_setup import DatabaseConfig


class TestUserCodeRouter(DatabaseConfig):
    def test_submit_custom_css(self):
        user = "beginbotbot"
        Command("damn").allow_user(user)
        result = UserCodeRouter(
            user,

            "css",
            ["https://gist.githubusercontent.com/davidbegin/raw/beginfun.css"],
        ).route()
        assert "Thanks for the custom CSS @beginbotbot!" in result

        css_filepath = Path(__file__).parent.parent.parent.joinpath(
            "build/beginworld_finance/styles/beginbotbot.css"
        )
        assert css_filepath.exists()

    def test_submit_custom_js(self):
        user = "beginbotbot"
        result = UserCodeRouter(
            user,
            "js",
            ["https://gist.githubusercontent.com/davidbegin/raw/beginfun.js"],
        ).route()
        assert "Thanks for the custom JS @beginbotbot!" in result

        js_filepath = Path(__file__).parent.parent.parent.joinpath(
            "chat_thief/js/beginfun.js"
        )
        assert js_filepath.exists()
        user_code = UserCode.last()
        assert user_code["user"] == "beginbotbot"
        assert (
            user_code["code_link"]
            == "https://gist.githubusercontent.com/davidbegin/raw/beginfun.js"
        )
        assert user_code["code_type"] == "js"

    def test_submit_custom_with_name(self):
        user = "beginbotbot"
        result = UserCodeRouter(
            user,
            "js",
            ["cool_widget", "https://gist.githubusercontent.com/davidbegin/raw"],
        ).route()
        assert "Thanks for the custom JS @beginbotbot!" in result

        js_filepath = Path(__file__).parent.parent.parent.joinpath(
            "chat_thief/js/beginbotbot.js"
        )
        assert js_filepath.exists()
        user_code = UserCode.last()
        assert user_code["user"] == "beginbotbot"
        assert user_code["name"] == "cool_widget"
        assert (
            user_code["code_link"]
            == "https://gist.githubusercontent.com/davidbegin/raw"
        )
        assert user_code["code_type"] == "js"

    def test_submit_custom_in_diff_order_js(self):
        user = "beginbotbot"
        result = UserCodeRouter(
            user,
            "js",
            ["https://gist.githubusercontent.com/davidbegin/raw", "cool_widget"],
        ).route()
        assert "Thanks for the custom JS @beginbotbot!" in result

        js_filepath = Path(__file__).parent.parent.parent.joinpath(
            "chat_thief/js/beginbotbot.js"
        )
        assert js_filepath.exists()
        user_code = UserCode.last()
        assert user_code["user"] == "beginbotbot"
        assert user_code["name"] == "cool_widget"
        assert (
            user_code["code_link"]
            == "https://gist.githubusercontent.com/davidbegin/raw"
        )
        assert user_code["code_type"] == "js"


    def test_submit_custom_js(self):
        user = "beginbotbot"
        result = UserCodeRouter(
            user, "js", ["https://gist.githubusercontent.com/davidbegin/raw"],
        ).route()
        assert "Thanks for the custom JS @beginbotbot!" in result

        js_filepath = Path(__file__).parent.parent.parent.joinpath(
            "chat_thief/js/beginbotbot.js"
        )
        assert js_filepath.exists()
        user_code = UserCode.last()
        assert user_code["user"] == "beginbotbot"
        assert (
            user_code["code_link"]
            == "https://gist.githubusercontent.com/davidbegin/raw"
        )
        assert user_code["code_type"] == "js"

    def test_updating_js(self):
        user = "beginbotbot"
        result = UserCodeRouter(
            user,
            "js",
            ["https://gist.githubusercontent.com/davidbegin/raw/beginfun.js"],
        ).route()
        assert UserCode.count() == 1

        UserCode.approve(user, "beginfun")
        user_code = UserCode.last()
        assert user_code["approved"] == True

        result = UserCodeRouter(
            user,
            "js",
            ["https://gist.githubusercontent.com/davidbegin/raw/234232342/beginfun.js"],
        ).route()
        assert UserCode.count() == 1
        user_code = UserCode.last()
        assert user_code["user"] == "beginbotbot"
        assert user_code["approved"] == True
        assert (
            user_code["code_link"]
            == "https://gist.githubusercontent.com/davidbegin/raw/234232342/beginfun.js"
        )
        assert user_code["code_type"] == "js"

    def test_approving_js(self):
        UserCode(
            user="beginbotbot",
            code_link="https://gist.githubusercontent.com/davidbegin/raw/beginfun.js",
            code_type="js",
        ).save()
        result = UserCodeRouter("beginbotbot", "approvejs", ["beginfun"]).route()
        assert "@beginbotbot's beginfun.js has been approved!" in result

    def test_buy_js(self):
        user_code = UserCode(
            user="eno",
            code_link="https://gitlab.com/real_url/beginwidget.js",
            code_type="js",
            approved=True,
        ).save()
        result = UserCodeRouter("beginbotbot", "buyjs", ["beginwidget"]).route()
        assert result == "@beginbotbot bought beginwidget.js from @eno!"
        assert UserCode.find_owners("beginwidget") == ["eno", "beginbotbot"]

    def test_deactivate_js(self):
        user_code = UserCode(
            user="eno",
            code_link="https://gitlab.com/real_url/beginwidget.js",
            code_type="js",
            approved=True,
            owners=["beginbotbot"],
        ).save()
        UserPage.bootstrap_user_page(user="beginbotbot", widgets=["beginwidget"])

        result = UserCodeRouter("beginbotbot", "deactivate", ["beginwidget"]).route()
        user_page = UserPage.for_user("beginbotbot")
        assert user_page["widgets"] == {"beginwidget": False}
