import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command

from chat_thief.stitch_and_sort import StitchAndSort

from tests.support.database_setup import DatabaseConfig


class TestStitchandSort(DatabaseConfig):
    def test_stitchin_and_sortin(self):
        baldclap = User("baldclap")
        baldclap.update_cool_points(3)
        damn_cmd = Command("damn")
        Command("damn").allow_user("baldclap")
        custom_css = "https://gist.githubusercontent.com/davidbegin/sfkgsjh"
        baldclap.set_value("custom_css", custom_css)
        chain_cmd = Command("mchdtmd")
        chain_cmd.save()

        result = StitchAndSort().call()

        assert result["users"] == [
            {
                "name": "baldclap",
                "command_file": "baldclap.opus",
                "wealth": 4,
                "street_cred": 0,
                "cool_points": 3,
                "mana": 3,
                "custom_css": custom_css,
                "commands": ["damn"],

                "top_eight": [],
            }
        ]

        assert result["commands"] == [
            {
                "name": "damn",
                "user": "beginbot",
                "command_file": "damn.opus",
                "permitted_users": ["baldclap"],
                "health": 3,
                "cost": 1,
                "like_to_hate_ratio": 100,
            },
            {
                "name": "mchdtmd",
                "command_file": "mchdtmd.mp3",
                "user": "beginbot",
                "permitted_users": [],
                "health": 3,
                "cost": 1,
                "like_to_hate_ratio": 100,
            },
        ]
