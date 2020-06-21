from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.bot_vote import BotVote


class TribalCouncil(BaseDbModel):
    database_path = "db/tribal_council.json"
    table_name = "tribal_council"

    @classmethod
    def go_to_tribal(cls):
        votes = {}
        for vote in BotVote.db().all():
            bot_name = vote["bot"]
            votes[bot_name] = votes.get(bot_name, []) + [vote["user"]]
        TribalCouncil(votes).save()

    def __init__(self, votes):
        self._votes = votes

    def doc(self):
        return {"round": 1, "votes": self._votes}
