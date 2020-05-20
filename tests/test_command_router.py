import pytest

from chat_thief.command_router import CommandRouter
from chat_thief.models.command import Command
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.user import User
from chat_thief.config.log import logger

from tests.support.database_setup import DatabaseConfig
from tests.support.utils import setup_logger

logger = setup_logger()


class TestCommandRouter(DatabaseConfig):
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

    @pytest.mark.skip
    def test_buying_a_non_existent_sound(self, irc_msg):
        user = "thugga"
        User(user).update_cool_points(10)
        message = "!buy gibberish"
        irc_response = irc_msg(user, message)
        result = CommandRouter(irc_response, logger).build_response()
        assert result == "@thugga purchase failed, command !gibberish not found"

    @pytest.mark.skip
    def test_transferring_a_command_already_owned(self, irc_msg):
        transferrer = User("thugga")
        transferee = User("wheezy")

        damn_command = Command("damn")
        damn_command.allow_user(transferee.name)

        message = "!transfer !damn @wheezy"
        irc_response = irc_msg(transferrer.name, message)
        result = CommandRouter(irc_response, logger).build_response()
        assert result == "@wheezy already has accesss to !damn @thugga"

    def test_iasip(self, irc_msg):
        irc_response = irc_msg("beginbot", "!iasip The Gang Steals Kappa")
        CommandRouter(irc_response, logger).build_response()
        news = BreakingNews.last()
        assert news["scope"] == "The Gang Steals Kappa"
