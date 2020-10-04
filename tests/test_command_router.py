from pathlib import Path


import pytest

from chat_thief.command_router import CommandRouter
from chat_thief.config.log import logger
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.command import Command
from chat_thief.models.proposal import Proposal
from chat_thief.models.user import User
from chat_thief.models.user_event import UserEvent
from chat_thief.models.bot_vote import BotVote
from chat_thief.models.css_vote import CSSVote
from chat_thief.welcome_committee import WelcomeCommittee

from tests.support.database_setup import DatabaseConfig
from tests.support.utils import setup_logger

logger = setup_logger()


class TestCommandRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["miles.davis"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    @pytest.fixture
    def irc_msg(self):
        def _irc_msg(user, msg):
            return f":{user}!{user}@user.tmi.twitch.tv PRIVMSG #beginbot :{msg}"

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

    @pytest.mark.skip
    def test_iasip(self, irc_msg):
        irc_response = irc_msg("beginbot", "!iasip The Gang Steals Kappa")
        CommandRouter(irc_response, logger).build_response()
        news = BreakingNews.last()
        assert news["scope"] == "The Gang Steals Kappa"

    def test_propose(self, irc_msg):
        irc_response = irc_msg("beginbot", "!propose !iasip The Gang Steals Kappa")
        result = CommandRouter(irc_response, logger).build_response()
        assert "Thank you @beginbot for your proposal" in result
        last_proposal = Proposal.last()
        assert last_proposal["proposal"] == "The Gang Steals Kappa"
        assert last_proposal["command"] == "iasip"

    def test_support(self, irc_msg):
        # Creating a Proposal
        irc_response = irc_msg("beginbot", "!propose !iasip The Gang Steals Kappa")
        result = CommandRouter(irc_response, logger).build_response()

        # Supporting a Proposal
        irc_response = irc_msg("bill.evans", "!support beginbot")
        result = CommandRouter(irc_response, logger).build_response()
        assert "@beginbot Thanks You for the support @bill.evans" in result

    def test_stealing_non_existent_sfx(self, irc_msg):
        User("bill.evans").update_cool_points(10)
        irc_response = irc_msg("bill.evans", "!steal fakesound")
        result = CommandRouter(irc_response, logger).build_response()
        assert result != "@bill.evans stole from @None"

    # We aren't mocking out user here, properly
    # or failing for another reason
    @pytest.mark.skip
    def test_share_command(self, irc_msg, monkeypatch):
        def _mock_random_user(self):
            return "miles.davis"

        monkeypatch.setattr("EconomyRouter", "_random_user", _mock_random_user)

        user = User("bill.evans")
        Command("damn").allow_user("bill.evans")
        irc_response = irc_msg("bill.evans", "!share damn")
        result = CommandRouter(irc_response, logger).build_response()

        assert (
            "@bill.evans Not enough cool_points (0/1) to share !damn with @" in result
        )

    # We aren't finding the target user,
    # Because miles ain't valid
    def test_top_8_features(self, irc_msg):
        user = User("bill.evans")
        miles = User("miles.davis")
        miles.save()
        irc_response = irc_msg("bill.evans", "!top8 miles.davis")
        result = CommandRouter(irc_response, logger).build_response()
        assert result == "@miles.davis is now in @bill.evans's Top 8!"
        assert user.top_eight() == ["miles.davis"]

    def test_user_events(self, irc_msg):
        user = User("bill.evans")
        miles = User("miles.davis")
        miles.save()
        irc_response = irc_msg("bill.evans", "!top8 miles.davis")
        result = CommandRouter(irc_response, logger).build_response()

        last_event = UserEvent.last()
        assert last_event["user"] == "bill.evans"
        assert last_event["msg"] == "!top8 miles.davis"
        assert last_event["result"] == "@miles.davis is now in @bill.evans's Top 8!"
        assert last_event["command"] == "top8"

    def test_buying_event(self, irc_msg):
        user = User("bill.evans")
        user.update_cool_points(10)
        irc_response = irc_msg("bill.evans", "!buy gcc")
        result = CommandRouter(irc_response, logger).build_response()
        last_event = UserEvent.last()
        assert last_event["user"] == "bill.evans"
        assert last_event["msg"] == "!buy gcc"
        # assert last_event["cool_point_diff"] == -1

    def test_bestcss(self, irc_msg):
        user = User("bill.evans")
        icon = User("miles.davis").save()
        irc_response = irc_msg("bill.evans", "!bestcss miles.davis")
        result = CommandRouter(irc_response, logger).build_response()
        assert CSSVote.count() == 1
        assert (
            result == "Thank You @bill.evans for supporting Artists like @miles.davis"
        )

        irc_response = irc_msg("bill.evans", "!homepage")
        result = CommandRouter(irc_response, logger).build_response()
        assert result == "@miles.davis: 1"

    def test_buying_insurance(self, irc_msg):
        user = User("uzi")
        user.update_cool_points(10)
        irc_response = irc_msg("uzi", "!insurance")
        result = CommandRouter(irc_response, logger).build_response()
        assert user.insured()
        assert result == "@uzi thank you for purchasing insurance"

    def test_bot_survivor(self, irc_msg):
        user = User("uzi")
        user.save()
        User("uzibot").save()
        User.register_bot("uzibot", "don.cannon")
        irc_response = irc_msg("uzi", "!hatebot uzibot")
        result = CommandRouter(irc_response, logger).build_response()
        BotVote.count() == 1
        assert result == "Thank you for your vote @uzi"

    def test_submitting_js(self, irc_msg):
        user = User("uzi")
        user.save()
        irc_response = irc_msg("uzi", "!js https://gitlab.com/snippets/1990806/raw")
        result = CommandRouter(irc_response, logger).build_response()
        assert result == "Thanks for the custom JS @uzi!"
