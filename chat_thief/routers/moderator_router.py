import os

from chat_thief.routers.base_router import BaseRouter
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.the_fed import TheFed
from chat_thief.begin_fund import BeginFund
from chat_thief.data_scrubber import DataScrubber


class ModeratorRouter(BaseRouter):
    def route(self):
        if self.user in STREAM_GODS:
            if self.command == "nomeme":
                os.system("nomeme")
                return

            if self.command == "no_news":
                return BreakingNews.purge()

            if self.command == "do_over":
                return self._do_over()

            if self.command == "revive":
                if self.parser.target_sfx:
                    print(f"We are attempting to revive: !{self.parser.target_sfx}")
                    Command.find_or_create(self.parser.target_sfx)
                    return Command(self.parser.target_sfx).revive()
                elif self.parser.target_user:
                    return User(self.parser.target_user).revive()
                else:
                    print(f"Not Sure who or what to silence: {self.args}")

            if self.command == "silence":
                if self.parser.target_sfx:
                    print(f"We are attempting to silence: {self.target_sfx}")
                    return Command(self.parser.target_sfx).silence()
                elif self.parser.target_user:
                    print(f"We are attempting to silence: {self.parser.target_user}")
                    return User(self.parser.target_user).kill()
                else:
                    print(f"Not Sure who or what to silence: {self.args}")

        if self.command == "dropeffect" and self.user in STREAM_GODS:
            return BeginFund(
                target_user=self.parser.target_user,
                target_command=self.parser.target_sfx,
                amount=self.parser.amount,
            ).drop()

    def _do_over(self):
        print("WE ARE GOING FOR IT!")

        for user_name in [user["name"] for user in User.all()]:
            User(user_name).bankrupt()

        DataScrubber.purge_duplicate_users()
        DataScrubber.purge_theme_songs()
        DataScrubber.purge_duplicates()

        # This could be so much faster
        for command_name in Command.db().all():
            command_name = command_name["name"]
            print(command_name)
            command = Command(command_name)
            command_cost = command.cost()

            if command_cost < 2:
                command.set_value("cost", 1)
            else:
                new_cost = int(command_cost / 2)
                TheFed.collect_tax(new_cost)
                command.set_value("cost", new_cost)

        return "Society now must rebuild"
