import pytest

from chat_thief.command_parser import CommandParser
from chat_thief.models.command import Command
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

    def test_issue_with_no_info(self, irc_msg):
        irc_response = irc_msg("fake_user", "!issue")
        result = CommandParser(irc_response, logger).build_response()
        assert result == "@fake_user Must include a description of the !issue"

    def test_transferring_to_another_user(self, irc_msg):
        user = "thugga"
        Command("damn").allow_user(user)
        message = "!give damn beginbotbot"
        irc_response = irc_msg(user, message)
        result = CommandParser(irc_response, logger).build_response()
        assert result == [
            "@beginbotbot now has access to !damn",
            "@thugga lost access to !damn",
        ]
