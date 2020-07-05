from tinydb import Query  # type: ignore

from chat_thief.models.base_db_model import BaseDbModel


class BotVote(BaseDbModel):
    database_path = "db/bot_votes.json"
    table_name = "bot_votes"

    def __init__(self, user, bot):
        self._user = user
        self._bot = bot

    @classmethod
    def by_bot(cs):
        return self.get_by_category("bot")
        # votes = self.db().all()
        # import itertools
        # import operator
        # steal_events = UserEvent.db().search(Query().command == "steal")
        # thieves = itertools.groupby(steal_events, operator.itemgetter("user"))

    def doc(self):
        return {"user": self._user, "bot": self._bot}

    def create_or_update(self):
        old_vote = self.db().get(Query().user == self._user)
        if old_vote:
            result = self.db().update({"bot": self._bot}, doc_ids=[old_vote.doc_id])
            return result, "update"
        else:
            result = self.save()
            return result, "create"
