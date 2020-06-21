from chat_thief.models.base_db_model import BaseDbModel


class BotVote(BaseDbModel):
    database_path = "db/bot_votes.json"
    table_name = "bot_votes"

    def __init__(self, user, bot):
        self._user = user
        self._bot = bot

    def doc(self):
        return {"user": self._user, "bot": self._bot}
