from argparse import ArgumentParser

from tinydb import Query  # type: ignore

from chat_thief.config.log import logger
from chat_thief.command_router import CommandRouter
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.vote import Vote
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.notification import Notification
from chat_thief.models.the_fed import TheFed
from chat_thief.models.css_vote import CSSVote
from chat_thief.models.user_code import UserCode
from chat_thief.data_scrubber import DataScrubber

DEFAULT_MSG = "!add_perm ha johnnyutah"
DEFAULT_MSG =  "nice"



def _fake_irc_msg_builder(user, msg):
    return [f":{user}!{user}@user.tmi.twitch.tv", "PRIVMSG", "#beginbot", f":{msg}"]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--message", "-m", dest="message", default=DEFAULT_MSG)
    parser.add_argument("--user", "-u", dest="user", default="beginbotbot")
    parser.add_argument(
        "--breakpoint", "-b", dest="breakpoint", action="store_true", default=False
    )
    args = parser.parse_args()
    irc_response = _fake_irc_msg_builder(args.user, args.message)

    if args.breakpoint:
        # found_command = Proposal.db().get(Query().name == name)
        # found_command = Proposal.db().search(Query().user == "beginbot")
        breakpoint()
    elif response := CommandRouter(irc_response, logger).build_response():
        print(response)
    else:
        print("No Response")
