from chat_thief.models.base_db_model import BaseDbModel


class CSSVote(BaseDbModel):
    table_name = "votes"
    database_path = "db/votes.json"

    def __init__(self, voter, candidate, page="homepage"):
        self.voter = voter
        self.candidate = candidate
        self.page = page

    def doc(self):
        return {
            "voter": self.voter,
            "candidate": self.candidate,
            "page": self.page,
        }
