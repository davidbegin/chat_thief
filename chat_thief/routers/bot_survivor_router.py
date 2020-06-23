from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.bot_vote import BotVote
from chat_thief.models.user import User
from chat_thief.routers.base_router import BaseRouter


class BotSurvivorRouter(BaseRouter):
    def route(self):
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        if parser.target_user:
            potential_bot = User(parser.target_user)

            if potential_bot.is_bot():
                # We need to update vote for that user
                result = BotVote(self.user, potential_bot.name).create_or_update()
                return "Thank you for your vote @beginbotbot"
            else:
                return f"@{self.user} @{parser.target_user} is NOT A BOT!"
