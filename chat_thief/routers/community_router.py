import os

from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.proposal import Proposal
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.routers.base_router import BaseRouter


DEFAULT_SUPPORT_REQUIREMENT = 5


class CommunityRouter(BaseRouter):
    SUPPORT_REQUIREMENT = DEFAULT_SUPPORT_REQUIREMENT

    def route(self):
        print("Trying to Route in the CommunityRouter")

        if self.command == "propose":
            print("CommunityRouter#propose")
            # What if it's not more than one Arg???

            if len(self.args) > 1:
                return self._propose()
            else:
                print("CommunityRouter#propose not enough args")
        elif self.command in ["iasip", "alwayssunny"]:
            print("CommunityRouter#iasip")
            proposal = Proposal(
                user=self.user, command="iasip", proposal=" ".join(self.args),
            )
            proposal.save()
            return f"Thank you @{self.user} for your proposal"
        elif self.command == "support":
            print("CommunityRouter#support")
            return self._support()

    def _propose(self):
        proposed_command, *args = self.args

        if proposed_command.startswith("!"):
            proposed_command = proposed_command[1:]

            proposal = Proposal(
                user=self.user, command=proposed_command, proposal=" ".join(args),
            )
            proposal.save()
            if "TEST_MODE" not in os.environ:
                PlaySoundeffectRequest(user="beginbotbot", command="5minutes").save()
            return f"Thank you @{self.user} for your proposal. You have 5 minutes to get 5 supporters"

    def _support(self):
        if self.args:
            user = self.args[0]
        else:
            user = Proposal.last()["user"]

        if user.startswith("@"):
            user = user[1:]

        proposal = Proposal.find_by_user(user)

        if Proposal(user).is_expired():
            if proposal:
                print(f"Deleteing Expired Proposal from: {user}")
                Proposal.delete(proposal.doc_id)
            else:
                print(f"Did not find Proposal for {user}")
            return

        total_support = len(proposal["supporters"]) + 1

        if total_support >= self.SUPPORT_REQUIREMENT:
            BreakingNews(
                scope=proposal["proposal"], category=proposal["command"]
            ).save()

        if proposal:
            return Proposal.support(user, proposal.doc_id, self.user)
