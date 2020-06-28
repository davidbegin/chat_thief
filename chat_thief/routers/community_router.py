import os

from chat_thief.models.user import User
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.proposal import Proposal
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.notification import Notification


DEFAULT_SUPPORT_REQUIREMENT = 3


class CommunityRouter(BaseRouter):
    SUPPORT_REQUIREMENT = DEFAULT_SUPPORT_REQUIREMENT

    def top8(self):
        user = User(self.user)

        if self.parser.target_user:
            user.add_to_top_eight(self.parser.target_user)
            return f"@{self.parser.target_user} is now in @{self.user}'s Top 8!"
        else:
            raise ValueError(f"We have no target user to add to Top 8 {self.args}")

    def hate8(self):
        user = User(self.user)
        user.remove_from_top_eight(self.parser.target_user)
        return f"@{self.parser.target_user} is no longer in @{self.user}'s Top 8"

    def clear8(self):
        user = User(self.user)
        user.clear_top_eight()
        return f"@{self.user} doesn't need friends, they disappoint them."

    def route(self):

        if self.command == "top8":
            return self.top8()

        if self.command == "hate8":
            return self.hate8()

        if self.command == "clear8":
            return self.clear8()

        if self.command == "propose":
            print("CommunityRouter#propose")
            # What if it's not more than one Arg???

            if len(self.args) > 1:
                return self._propose()
            else:
                print("CommunityRouter#propose not enough args")
        elif self.command in ["iasip", "alwayssunny"]:
            return self._propose("iasip")

        elif self.command == "support":
            print("CommunityRouter#support")
            return self._support()

    def _propose(self, proposed_command=None):
        if proposed_command:
            args = self.args
        else:
            proposed_command, *args = self.args

        if proposed_command.startswith("!"):
            proposed_command = proposed_command[1:]

        proposal = Proposal(
            user=self.user, command=proposed_command, proposal=" ".join(args),
        )
        proposal.save()

        if "TEST_MODE" not in os.environ:
            # Maybe I should be able to say no notification

            PlaySoundeffectRequest(
                user="beginbotbot", command="5minutes", notification=False
            ).save()

            Notification("Type !support", duration=300).save()
        return f"Thank you @{self.user} for your proposal. You have 5 minutes to get {self.SUPPORT_REQUIREMENT} supporters"

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

        total_support = len(proposal["supporters"]) + 1

        support_msg = ""
        if proposal:
            support_msg = Proposal.support(user, proposal.doc_id, self.user)

        if total_support >= self.SUPPORT_REQUIREMENT:
            BreakingNews(
                scope=proposal["proposal"], category=proposal["command"]
            ).save()
            if proposal:
                print(f"Deleteing Proposal from: {user}, since it was approved!")
                Proposal.delete(proposal.doc_id)

        return support_msg + f" {total_support}/{self.SUPPORT_REQUIREMENT}"
