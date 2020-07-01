import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command

from chat_thief.stitch_and_sort import StitchAndSort

from tests.support.database_setup import DatabaseConfig


class TestStitchandSort(DatabaseConfig):
    def test_stitchin_and_sortin(self):
        baldclap = User("baldclap")
        baldclap.update_cool_points(3)
        baldclap.update_cool_points(1)

        Command("damn").allow_user("baldclap")

        momoko = User("momoko")
        mclovin = Command("mclovin")
        mclovin.allow_user(momoko.name)

        damn_cmd = Command("damn")

        custom_css = "https://gist.githubusercontent.com/davidbegin/sfkgsjh"
        baldclap.set_value("custom_css", custom_css)
        chain_cmd = Command("mchdtmd")
        chain_cmd.save()

        result = StitchAndSort().call()

        assert result["users"][0] == {
            "name": "baldclap",
            "command_file": "baldclap.opus",
            "wealth": 5,
            "insured": False,
            "street_cred": 0,
            "cool_points": 4,
            "mana": 3,
            "custom_css": custom_css,
            "widgets": {"approved": [], "unapproved": [], "deactivated": []},
            "commands": [
                {
                    "name": "damn",
                    "user": "beginbot",
                    "permitted_users": ["baldclap"],
                    "health": 3,
                    "cost": 1,
                    "command_file": "damn.opus",
                    "like_to_hate_ratio": 100,
                }
            ],
            "sfx_count": 1,
            "top_eight": [],
        }
        assert result["users"][1] == {
            "name": "momoko",
            "custom_css": None,
            "street_cred": 0,
            "cool_points": 0,
            "insured": False,
            "mana": 3,
            "top_eight": [],
            "wealth": 1,
            "widgets": {"approved": [], "unapproved": [], "deactivated": []},
            "sfx_count": 1,
            "commands": [
                {
                    "name": "mclovin",
                    "user": "beginbot",
                    "permitted_users": ["momoko"],
                    "health": 3,
                    "cost": 1,
                    "command_file": "mclovin.opus",
                    "like_to_hate_ratio": 100,
                }
            ],
        }

        assert {
            "name": "mclovin",
            "user": "beginbot",
            "permitted_users": ["momoko"],
            "health": 3,
            "cost": 1,
            "command_file": "mclovin.opus",
            "like_to_hate_ratio": 100,
        } in result["commands"]

        assert {
            "name": "damn",
            "user": "beginbot",
            "permitted_users": ["baldclap"],
            "health": 3,
            "cost": 1,
            "command_file": "damn.opus",
            "like_to_hate_ratio": 100,
        } in result["commands"]

        assert {
            "name": "mchdtmd",
            "user": "beginbot",
            "permitted_users": [],
            "health": 3,
            "cost": 1,
            "command_file": "mchdtmd.mp3",
            "like_to_hate_ratio": 100,
        } in result["commands"]
