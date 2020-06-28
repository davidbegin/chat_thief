from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.models.bot_vote import BotVote
from chat_thief.models.user import User
from chat_thief.models.tribal_council import TribalCouncil
from chat_thief.routers.base_router import BaseRouter


class BotSurvivorRouter(BaseRouter):
    def route(self):
        if self.command in ["hatebot", "votebotout"]:
            if self.parser.target_user:
                potential_bot = User(self.parser.target_user)

                if potential_bot.is_bot():
                    # We need to update vote for that user
                    result = BotVote(self.user, potential_bot.name).create_or_update()
                    return f"Thank you for your vote @{self.user}"
                else:
                    return f"@{self.user} @{self.parser.target_user} is NOT A BOT!"

        if self.command == "tribal_council" and self.user == "beginbotbot":
            print("TRIBAL COUNCIL TIME!!!")
            # result = TribalCouncil.go_to_tribal()
            loser = BotVote.count_by_group("bot")[0][0]
            return f"@{loser} has been kicked out of BeginWorld"
