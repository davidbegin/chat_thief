from chat_thief.routers.base_router import BaseRouter
from chat_thief.prize_dropper import drop_soundeffect, dropreward
from chat_thief.commands.airdrop import Airdrop
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.breaking_news import BreakingNews


class ModeratorRouter(BaseRouter):
    def route(self):
        print("Looking for Commands in ModeratorRouter")

        if self.user in STREAM_GODS:
            if self.command == "no_news":
                return BreakingNews.purge()

            if self.command == "do_over":
                print("WE ARE GOING FOR IT!")
                for user in User.all():
                    User(user).bankrupt()
                for command_name in Command.db().all():
                    command_name = command_name["name"]
                    print(command_name)
                    command = Command(command_name)
                    for user in command.users():
                        print(command.unallow_user(user))
                return "Society now must rebuild"

            if self.command == "revive":
                parser = CommandParser(
                    user=self.user, command=self.command, args=self.args
                ).parse()

                if parser.target_sfx:
                    print(f"We are attempting to revive: !{parser.target_sfx}")
                    Command.find_or_create(parser.target_sfx)
                    return Command(parser.target_sfx).revive()
                elif parser.target_user:
                    return User(parser.target_user).revive()
                else:
                    print(f"Not Sure who or what to silence: {self.args}")

            if self.command == "silence":
                parser = CommandParser(
                    user=self.user, command=self.command, args=self.args
                ).parse()

                if parser.target_sfx:
                    print(f"We are attempting to silence: {self.target_sfx}")
                    return Command(parser.target_sfx).silence()
                elif parser.target_user:
                    print(f"We are attempting to silence: {parser.target_user}")
                    return User(parser.target_user).kill()
                else:
                    print(f"Not Sure who or what to silence: {self.args}")

        if self.command == "dropeffect" and self.user in STREAM_GODS:
            parser = CommandParser(
                user=self.user, command=self.command, args=self.args
            ).parse()

            return Airdrop(
                target_user=parser.target_user,
                target_command=parser.target_sfx,
                amount=parser.amount,
            ).drop()

        if self.command == "dropreward" and self.user in STREAM_GODS:
            return dropreward()
