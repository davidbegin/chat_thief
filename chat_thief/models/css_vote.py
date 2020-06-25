import itertools
import operator

from chat_thief.models.base_db_model import BaseDbModel


class CSSVote(BaseDbModel):
    table_name = "css_votes"
    database_path = "db/css_votes.json"

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

    @classmethod
    def by_votes(cls):
        votes = cls.db().all()
        votes_by_candidate = itertools.groupby(
            votes, operator.itemgetter("candidate")
        )
        vote_counts = [
            (candidate, len(list(votes)))
            for (candidate, votes) in votes_by_candidate
        ]
        return list(reversed(
            sorted(vote_counts, key=lambda vote: vote[1])
        ))

