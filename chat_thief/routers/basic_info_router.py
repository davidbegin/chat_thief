from chat_thief.commands.la_libre import LaLibre
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.user import User


class BasicInfoRouter:
    def __init__(self, user, command, args=[]):
        self.user = user
        self.command = command
        self.args = args

    def route(self):
        if self.command == "la_libre":
            return LaLibre.inform()

        if self.command == "streamlords":
            return " ".join(STREAM_LORDS)

        if self.command == "streamgods":
            return " ".join(STREAM_GODS)

        if self.command == "so":
            return self._shoutout()

        if self.user in STREAM_GODS:
            parser = CommandParser(
                user=self.user, command=self.command, args=self.args
            ).parse()

            if self.command == "bankrupt":
                return User(parser.target_user).bankrupt()

            if self.command == "paperup":
                return User(parser.target_user).paperup()

    def _shoutout(self):
        return f"Shoutout twitch.tv/{self.args[0]}"
