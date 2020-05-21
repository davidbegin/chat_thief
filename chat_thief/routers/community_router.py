from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.proposal import Proposal

from chat_thief.chat_parsers.command_parser import CommandParser


class CommunityRouter(BaseRouter):
    def route(self):

        # CommandParser(self.user, command)

        if self.command == "propose":
            if len(self.args) > 1:
                proposed_command, *args = self.args

                if proposed_command.startswith("!"):
                    proposed_command = proposed_command[1:]

                    proposal = Proposal(
                        user=self.user,
                        command=proposed_command,
                        proposal=" ".join(args),
                    )
                    proposal.save()
                    return f"Thank you @{self.user} for your proposal"

        elif self.command == "support":
            user = self.args[0]
            if user.startswith("@"):
                user = user[1:]

            proposal = Proposal.find_by_user(user)

            if proposal:
                return Proposal.support(user, proposal.doc_id, self.user)
