from pathlib import Path
import random

import pytest

from chat_thief.routers.economy_router import EconomyRouter
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.current_stream import CurrentStream

from tests.support.database_setup import DatabaseConfig


class TestEconomyRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def control_chaos(self):
        random.seed(0)

    @pytest.fixture
    def mock_find_random_user(self, monkeypatch):
        users = ["birdman", "wheezy", "young.thug", "future"]

        def _fake_find_random_user(self):
            return users.pop()

        monkeypatch.setattr(EconomyRouter, "_random_user", _fake_find_random_user)
        monkeypatch.setattr(StreetCredTransfer, "_random_user", _fake_find_random_user)

    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["not_streamlord", "young.thug", "uzi", "uzibot"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    def test_me(self):
        result = EconomyRouter("beginbotbot", "me", []).route()
        assert "beginbotbot" in result
        assert "Wealth" in result

    def test_perms(self):
        result = EconomyRouter("beginbotbot", "perms", ["clap"]).route()
        assert (
            result
            == "!clap | Cost: 1 | Health: 3 | Like Ratio 100% | https://mygeoangelfirespace.city/commands/clap.html"
        )

    def test_donate(self, mock_present_users, mock_find_random_user):
        user = User("uzi")
        User("young.thug").save()
        Command("clap").allow_user(user.name)
        assert "uzi" in Command("clap").users()
        assert "young.thug" not in Command("clap").users()
        result = EconomyRouter("uzi", "donate", ["young.thug"]).route()
        assert "young.thug" in Command("clap").users()
        assert "uzi" not in Command("clap").users()
        assert "was gifted" in result

    def test_hate_and_like_command(self):
        assert SFXVote("clap").supporter_count() == 0
        assert SFXVote("clap").detractor_count() == 0
        result = EconomyRouter("thugga", "like", ["clap"]).route()
        assert SFXVote("clap").supporter_count() == 1
        result = EconomyRouter("future", "hate", ["clap"]).route()
        assert SFXVote("clap").detractor_count() == 1

    def test_you_cannot_love_yourself(self):
        user = "young.thug"
        User("young.thug").save()
        result = EconomyRouter("young.thug", "love", ["@young.thug"]).route()
        assert (
            result
            == "You can love yourself in real life, but not in Beginworld @young.thug"
        )

    def test_you_cannot_props_ya_bot(self):
        creator = User("uzi").save()
        User("uzi").update_street_cred(10)
        bot = User("uzibot").save()
        User.register_bot("uzibot", "uzi")
        result = EconomyRouter("uzi", "props", ["uzibot"]).route()
        assert result == "You cannot props your own bot @uzi @uzibot"

    def test_ya_bot_cannot_props_you(self):
        creator = User("uzi").save()
        bot = User("uzibot").save()
        User("uzi").update_street_cred(10)
        User.register_bot("uzibot", "uzi")
        result = EconomyRouter("uzibot", "props", ["uzi"]).route()
        assert result == "You cannot props your creator @uzibot @uzi"

    def test_all_props(self):
        young_thug = User("young.thug")
        young_thug.update_street_cred(10)
        uzi = User("uzi")
        result = EconomyRouter(young_thug.name, "props", [uzi.name, "all"]).route()
        assert young_thug.cool_points() == 0
        assert young_thug.street_cred() == 0
        assert uzi.cool_points() == 10

    def test_props(self):
        young_thug = User("young.thug")
        uzi = User("uzi")

        uzi.update_street_cred(10)

        assert young_thug.cool_points() == 0
        assert young_thug.street_cred() == 0
        assert uzi.street_cred() == 10

        result = EconomyRouter(uzi.name, "props", [young_thug.name]).route()
        assert young_thug.cool_points() == 1
        assert young_thug.street_cred() == 0
        assert uzi.street_cred() == 9

    def test_props_random(self, mock_find_random_user):
        uzi = User("uzi")
        uzi.update_street_cred(10)
        uzi.add_to_top_eight("future")
        uzi.add_to_top_eight("young.thug")
        uzi.add_to_top_eight("wheezy")
        result = EconomyRouter(uzi.name, "props", ["random", "2"]).route()
        assert result == "@uzi gave 1 Street Cred to @future @young.thug each"
        result = EconomyRouter(uzi.name, "props", ["random"]).route()
        assert result == "@uzi gave 1 Street Cred to @wheezy"

    def test_props_with_no_top_eigth(self):
        uzi = User("uzi")
        result = EconomyRouter(uzi.name, "props", ["random"]).route()
        return result == "You must specify a Top8 to give random props. !top8 @user"

    def test_steal_with_no_params(self):
        user = User("beginbot")
        result = EconomyRouter(user.name, "steal", []).route()
        assert result == "@beginbot you must specify who and what you want to steal."

    def test_stealing_from_your_own_bot(self, mock_present_users):
        creator = User("uzi").save()
        bot = User("uzibot").save()
        Command("clap").allow_user("uzibot")
        User.register_bot("uzibot", "uzi")
        result = EconomyRouter("uzi", "steal", ["uzibot", "clap"]).route()
        assert result == "You cannot steal from your own bot @uzi @uzibot"

    def test_your_bot_stealing_from_you(self, mock_present_users):
        creator = User("uzi").save()
        bot = User("uzibot").save()
        Command("clap").allow_user("uzi")
        User.register_bot("uzibot", "uzi")
        result = EconomyRouter("uzibot", "steal", ["uzi", "clap"]).route()
        assert result == "You cannot steal from your creator @uzibot @uzi"

    def test_try_steal_fake_sound(self, mock_present_users, mock_find_random_user):
        User("uzi").update_cool_points(10)
        Command("clap").allow_user("uzi")
        user = User("young.thug")
        user.update_cool_points(10)
        result = EconomyRouter(user.name, "steal", ["fakesound"]).route()
        assert (
            result
            == "@young.thug you must specify who and what you want to steal. Invalid Args: fakesound"
        )
        assert user.cool_points() == 10

    def test_try_steal_unowned_sound(self, mock_present_users, mock_find_random_user):
        User("uzi").update_cool_points(10)
        user = User("young.thug")
        user.update_cool_points(10)
        result = EconomyRouter(user.name, "steal", ["clap", "uzi"]).route()
        assert result == "!clap is not owned by @uzi"
        assert user.cool_points() == 10

    def test_buying_random(self, mock_find_random_user):
        user = "young.thug"
        User(user).update_cool_points(10)
        result = EconomyRouter(user, "buy", ["clap"]).route()

        # This returns a Result Object right now
        # We have not decided all the proper boundaries
        # assert "@young.thug bought 1 SFXs: !clap" in result
        assert User(user).cool_points() < 10

    def test_buy_more_than_one_random(self):
        user = User("young.thug")
        user.update_cool_points(10)
        assert user.commands() == []
        result = EconomyRouter(user.name, "buy", ["random", 3]).route()
        assert len(user.commands()) == 3
        assert user.cool_points() < 10

    def test_transferring_to_another_user(self, mock_find_random_user):
        user = "young.thug"
        User("uzi").save()
        User(user).update_cool_points(10)
        command = Command("damn")
        command.allow_user(user)
        result = EconomyRouter(user, "give", ["damn", "uzi"]).route()
        assert result == [
            "@uzi now has access to !damn",
            "@young.thug lost access to !damn",
        ]

    def test_sharing_with_another_user(self, monkeypatch):
        def fake_random_user(self):
            return users.pop()

        monkeypatch.setattr(CurrentStream, "random_user", fake_random_user)

        user = "young.thug"
        User("uzi").save()
        User(user).update_cool_points(10)
        command = Command("damn")
        command.allow_user(user)
        result = EconomyRouter(user, "share", ["damn", "uzi"]).route()
        assert result == "young.thug shared @uzi now has access to !damn"

    def test_submit_custom_css(self):
        user = "beginbotbot"
        User(user).update_cool_points(10)
        command = Command("damn")
        command.allow_user(user)
        result = EconomyRouter(
            user,
            "css",
            ["https://gist.githubusercontent.com/davidbegin/raw/beginfun.css"],
        ).route()
        assert "Thanks for the custom CSS @beginbotbot!" in result

        css_filepath = Path(__file__).parent.parent.parent.joinpath(
            "build/beginworld_finance/styles/beginbotbot.css"
        )
        assert css_filepath.exists()
