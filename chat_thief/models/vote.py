DEFAULT_VOTES_DB_PATH = "db/votes.json"
from chat_thief.models.database import db_table

from tinydb import Query

class Vote:
    def __init__(self, user, votes_db_path=DEFAULT_VOTES_DB_PATH):
        self.votes_db = db_table(votes_db_path, "votes")
        self.user = user

    # When theres a certain percentage of users
    # We are going to create 3 Users
    # Then we are going to vote, 2 times
    # and make sure the 2nd time triggers resolution
    def have_tables_turned(self, threshold):
        if self.revolution_count() > threshold:
            return "revolution"

        if self.peace_count() > threshold:
            return "peace"

        return False


    def vote_count(self):
        return len(self.votes_db.all())

    def revolution_count(self):
        return len(self.votes_db.search(Query().vote == "revolution"))

    def peace_count(self):
        # this Query is being cached??
        return len(self.votes_db.search(Query().vote == "peace"))

    def vote(self, vote):
        user = self._find_user()

        def user_vote(new_vote):
            def transform(doc):
                doc["vote"] = new_vote
            return transform

        if user:
            print(f"Previous Vote for User {self.user}!")
            self.votes_db.update(user_vote(vote), Query().user == self.user)
        else:
            print(f"NO Previous Vote for User {self.user}!")
            from tinyrecord import transaction
            with transaction(self.votes_db) as tr:
                tr.insert(self.doc(vote))
            self.doc(vote)

        return {"Revolution": self.revolution_count(), "Peace": self.peace_count()}


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
