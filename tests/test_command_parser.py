import pytest

from chat_thief.command_parser import CommandParser
from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.config.log import logger

from tests.support.database_setup import DatabaseConfig
from tests.support.utils import setup_logger

logger = setup_logger()


class TestCommandParser(DatabaseConfig):
    @pytest.fixture
    def irc_msg(self):
        def _irc_msg(user, msg):
            return [
                f":{user}!{user}@user.tmi.twitch.tv",
                "PRIVMSG",
                "#beginbot",
                f":{msg}",
            ]

        return _irc_msg

    @pytest.fixture
    def mock_find_random_user(self, monkeypatch):
        def _fake_find_random_user(self):
            return "thugga"

        # monkeypatch.setattr(obj, name, value, raising=True)
        monkeypatch.setattr(
            CommandParser, "random_not_you_user", _fake_find_random_user
        )

    def test_issue_with_no_info(self, irc_msg):
        irc_response = irc_msg("fake_user", "!issue")
        result = CommandParser(irc_response, logger).build_response()
        assert result == "@fake_user Must include a description of the !issue"

    def test_transferring_to_another_user(self, irc_msg):
        user = "thugga"
        User(user).update_cool_points(10)
        command = Command("damn")
        command.allow_user(user)
        message = "!give damn beginbot"
        irc_response = irc_msg(user, message)
        result = CommandParser(irc_response, logger).build_response()
        assert result == [
            "@beginbot now has access to !damn",
            "@thugga lost access to !damn",
        ]

    @pytest.mark.skip
    def test_buying_a_non_existent_sound(self, irc_msg):
        user = "thugga"
        User(user).update_cool_points(10)
        message = "!buy gibberish"
        irc_response = irc_msg(user, message)
        result = CommandParser(irc_response, logger).build_response()
        assert result == "@thugga purchase failed, command !gibberish not found"

    def test_buying_random(self, irc_msg):
        user = "thugga"
        User(user).update_cool_points(10)
        message = "!buy clap"
        irc_response = irc_msg(user, message)
        result = CommandParser(irc_response, logger).build_response()
        assert result == "@thugga bought !clap"
        assert User(user).cool_points() < 10

    def test_you_cannot_love_yourself(self, irc_msg):
        user = "thugga"
        message = "!love thugga"
        irc_response = irc_msg(user, message)
        result = CommandParser(irc_response, logger).build_response()
        assert (
            result
            == "You can love yourself in real life, but not in Beginworld @thugga"
        )

    @pytest.mark.skip
    def test_transferring_a_command_already_owned(self, irc_msg):
        transferrer = User("thugga")
        transferee = User("wheezy")

        damn_command = Command("damn")
        damn_command.allow_user(transferee.name)

        message = "!transfer !damn @wheezy"
        irc_response = irc_msg(transferrer.name, message)
        result = CommandParser(irc_response, logger).build_response()
        assert result == "@wheezy already has accesss to !damn @thugga"

    def test_steal_with_no_params(self, irc_msg, mock_find_random_user):
        thugga = User("thugga")
        thugga.update_cool_points(10)
        Command("damn").allow_user("thugga")
        user = User("beginbot")
        user.update_cool_points(10)

        message = "!steal"
        irc_response = irc_msg(user.name, message)
        result = CommandParser(irc_response, logger).build_response()
        assert result != "@beginbot stole from !damn from @thugga"
