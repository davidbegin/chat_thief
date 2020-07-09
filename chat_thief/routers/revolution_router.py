from typing import Optional

from chat_thief.routers.base_router import BaseRouter  # type: ignore
from chat_thief.models.vote import Vote  # type: ignore
from chat_thief.commands.la_libre import LaLibre  # type: ignore
from chat_thief.commands.revolution import Revolution  # type: ignore


class RevolutionRouter(BaseRouter):
    def route(self) -> Optional[str]:
        if self.command == "coup":
            threshold = LaLibre.threshold()
            result = Vote.have_tables_turned(threshold)
            print(f"The Result of have_tables_turned: {result}")

            if result in ["peace", "revolution"]:
                return Revolution(self.user).attempt_coup(result)
            else:
                return f"The Will of the People have not chosen: {threshold} votes must be cast for either Peace or Revolution"

        if self.command in ["peace", "revolution", "vote"]:
            if self.command == "vote":
                vote = self.args[0]
                Vote(user=self.user).vote(vote)
            else:
                Vote(user=self.user).vote(self.command)
            return f"Thank you for your vote @{self.user}"
