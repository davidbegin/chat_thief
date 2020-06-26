from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.bot_vote import BotVote


class TribalCouncil(BaseDbModel):
    database_path = "db/tribal_council.json"
    table_name = "tribal_council"

    @classmethod
    def go_to_tribal(cls):
        votes = {}
        votes_ids = []
        for vote in BotVote.db().all():
            bot_name = vote["bot"]
            votes_ids.append(vote.doc_id)
            votes[bot_name] = votes.get(bot_name, []) + [vote["user"]]

        council_numbers = [
            council["council_number"] for council in TribalCouncil.db().all()
        ]
        if council_numbers:
            last_council_number = max(council_numbers) + 1
        else:
            last_council_number = 1

        TribalCouncil(votes, last_council_number).save()
        BotVote.db().remove(doc_ids=votes_ids)

    def __init__(self, votes, council_number=1):
        self._votes = votes
        self._council_number = council_number

    def doc(self):
        return {"council_number": self._council_number, "votes": self._votes}
