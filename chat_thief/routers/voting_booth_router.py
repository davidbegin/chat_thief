import itertools
import operator

from chat_thief.routers.base_router import BaseRouter
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.css_vote import CSSVote


class VotingBoothRouter(BaseRouter):
    def route(self):
        if self.command == "bestcss":
            if self.parser.target_user:
                result = CSSVote(
                    voter=self.user, candidate=self.parser.target_user
                ).create_or_update()
                return f"Thank You @{self.user} for supporting Artists like @{self.parser.target_user}"
        elif self.command == "homepage":
            return " | ".join(
                [f"@{candidate}: {count}" for (candidate, count) in CSSVote.by_votes()]
            )
