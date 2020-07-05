import itertools
import operator

from tinydb import Query  # type: ignore

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

    def create_or_update(self):
        if old_vote := self.db().get(Query().voter == self.voter):
            result = self.db().update(self.doc(), doc_ids=[old_vote.doc_id])
            return result, "update"
        else:
            result = self.save()
            return result, "create"

    @classmethod
    def by_votes(cls):
        votes = cls.db().all()

        def get_candidate(vote):
            return vote.get("candidate")

        votes_by_candidate = itertools.groupby(
            sorted(votes, key=get_candidate), get_candidate
        )

        vote_counts = [
            (candidate, len(list(votes))) for (candidate, votes) in votes_by_candidate
        ]
        return list(reversed(sorted(vote_counts, key=lambda vote: vote[1])))
