import itertools
import operator

from chat_thief.routers.base_router import BaseRouter
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.css_vote import CSSVote


class VotingBoothRouter(BaseRouter):
    def route(self):
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        if self.command == "bestcss":
            if parser.target_user:
                result = CSSVote(
                    voter=self.user, candidate=parser.target_user
                ).create_or_update()
                return f"Thank You @{self.user} for supporting Artists like @{parser.target_user}"
        elif self.command == "homepage":
            return " | ".join(
                [f"@{candidate}: {count}" for (candidate, count) in CSSVote.by_votes()]
            )
