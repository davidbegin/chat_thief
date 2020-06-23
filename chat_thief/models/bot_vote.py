from tinydb import Query

from chat_thief.models.base_db_model import BaseDbModel


# Validation at the object level
#   - we have to search through all the objects
#
# Validation at the routing
#   - One Look up

# def validate_unique(doc_func, field):
#     breakpoint()
#     def wrapper():
#         return doc_func
#     return wrapper


class BotVote(BaseDbModel):
    database_path = "db/bot_votes.json"
    table_name = "bot_votes"

    def __init__(self, user, bot):
        self._user = user
        self._bot = bot

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
