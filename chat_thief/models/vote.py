DEFAULT_VOTES_DB_PATH = "db/votes.json"
from chat_thief.models.database import db_table

from tinydb import Query


class Vote:
    table_name = "votes"
    database_folder = ""
    database_path = "db/votes.json"

    def __init__(self, user):
        self.user = user

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def peace_keepers(self):
        return [vote["user"] for vote in self.db().search(Query().vote == "peace")]

    def revolutionaries(self):
        return [
            freedom_fighter["user"]
            for freedom_fighter in self.db().search(Query().vote == "revolution")
        ]

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
        return len(self.db().all())

    def revolution_count(self):
        return len(self.revolutionaries())

    def peace_count(self):
        return len(self.peace_keepers())

    def vote(self, vote):
        user = self._find_user()

        def user_vote(new_vote):
            def transform(doc):
                doc["vote"] = new_vote

            return transform

        if user:
            print(f"Previous Vote for User {self.user}!")
            self.db().update(user_vote(vote), Query().user == self.user)
        else:
            print(f"NO Previous Vote for User {self.user}!")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc(vote))
            self.doc(vote)

        return {"Revolution": self.revolution_count(), "Peace": self.peace_count()}

    def doc(self, vote):
        return {"user": self.user, "vote": vote}

    def _find_user(self):
        user = self.db().search(Query().user == self.user)

        if user:
            print("We Found a user!")
            return user[-1]
