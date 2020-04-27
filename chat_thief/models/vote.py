DEFAULT_VOTES_DB_PATH = "db/votes.json"
from chat_thief.models.database import db_table

from tinydb import Query

class Vote:
    def __init__(self, user,
            votes_db_path=DEFAULT_VOTES_DB_PATH):
        self.votes_db = db_table(votes_db_path, "votes")
        self.user = user

    def vote_count(self):
        return len(self.votes_db.all())

    def revolution_count(self):
        return len(self.votes_db.search(Query().vote == "revolution"))

    def peace_count(self):
        return len(self.votes_db.search(Query().vote == "peace"))

    def vote(self, vote):
        user = self._find_user()

        def user_vote(new_vote):
            def transform(doc):
                doc["vote"] = new_vote
            return transform

        if user:
            return self.votes_db.update(user_vote(vote), Query().user == self.user)
        else:
            print("NO user!")
            from tinyrecord import transaction
            with transaction(self.votes_db) as tr:
                tr.insert(self.doc(vote))
            return self.doc(vote)


    def doc(self, vote):
        return {
            "user": self.user,
            "vote": vote
        }


    def _find_user(self):
        user = self.votes_db.search(Query().user == self.user)

        if user:
            print("We Found a user!")
            return user[-1]
