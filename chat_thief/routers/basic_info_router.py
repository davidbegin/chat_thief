from urllib.parse import quote

from chat_thief.commands.la_libre import LaLibre
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.user import User
from chat_thief.routers.base_router import BaseRouter


class BasicInfoRouter(BaseRouter):
    def route(self):
        if self.command == "la_libre":
            return " | ".join(LaLibre.inform())

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
                if parser.target_user:
                    return User(parser.target_user).paperup()
                else:
                    return "You need to specify who to Paperup"

    def _shoutout(self):
        user_path = self.args[0]
        if user_path.startswith("@"):
            user_path = user_path[1:]
        return f"Shoutout twitch.tv/{quote(user_path)}"
