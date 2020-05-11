DEFAULT_VOTES_DB_PATH = "db/votes.json"
from chat_thief.models.database import db_table
from chat_thief.models.user import User

from chat_thief.config.log import error, warning, success

from tinydb import Query
from chat_thief.models.base_model import BaseModel


class Vote(BaseModel):
    table_name = "votes"
    database_path = "db/votes.json"

    @classmethod
    def peace_keepers(cls):
        return [vote["user"] for vote in cls.db().search(Query().vote == "peace")]

    @classmethod
    def revolutionaries(cls):
        return [
            freedom_fighter["user"]
            for freedom_fighter in cls.db().search(Query().vote == "revolution")
        ]

    @classmethod
    def voters(cls):
        return [vote["user"] for vote in cls.db().all()]

    @classmethod
    def fence_sitters(cls):
        return list(set(User.all()) - set(cls.voters()))

    # When theres a certain percentage of users
    # We are going to create 3 Users
    # Then we are going to vote, 2 times
    # and make sure the 2nd time triggers resolution
    @classmethod
    def have_tables_turned(cls, threshold):
        rev_count = cls.revolution_count()
        peace_count = cls.peace_count()

        if rev_count > peace_count:
            if rev_count >= threshold:
                return "revolution"
        if peace_count > rev_count:
            if peace_count >= threshold:
                return "peace"

        return False

    @classmethod
    def vote_count(cls):
        return len(cls.db().all())

    @classmethod
    def revolution_count(cls):
        return len(cls.revolutionaries())

    @classmethod
    def peace_count(cls):
        return len(cls.peace_keepers())

    def __init__(self, user):
        self.user = user

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
            warning(f"NO Previous Vote for User {self.user}!")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc(vote))
            # self.doc(vote)

        return {"Revolution": self.revolution_count(), "Peace": self.peace_count()}

    def doc(self, vote):
        return {"user": self.user, "vote": vote}

    def _find_user(self):
        user = self.db().search(Query().user == self.user)

        if user:
            print("We Found a user!")
            return user[-1]
