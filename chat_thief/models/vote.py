from typing import Optional, List, Any, Dict, Callable

from tinydb import Query  # type: ignore

from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.user import User
from chat_thief.config.log import error, warning, success
from chat_thief.models.transaction import transaction


class Vote(BaseDbModel):
    table_name = "votes"
    database_path = "db/votes.json"

    def __init__(self, user: str, vote: Optional[str] = None):
        self.user = user
        self._vote = vote

    def doc(self) -> Dict:
        return {"user": self.user, "vote": self._vote}

    @classmethod
    def peace_keepers(cls) -> List[str]:
        return [vote["user"] for vote in cls.db().search(Query().vote == "peace")]

    @classmethod
    def revolutionaries(cls) -> List[str]:
        return [
            freedom_fighter["user"]
            for freedom_fighter in cls.db().search(Query().vote == "revolution")
        ]

    @classmethod
    def voters(cls) -> List[str]:
        return [vote["user"] for vote in cls.db().all()]

    @classmethod
    def fence_sitters(cls) -> List[str]:
        return list(set([user["name"] for user in User.all()]) - set(cls.voters()))

    # When theres a certain percentage of users
    # We are going to create 3 Users
    # Then we are going to vote, 2 times
    # and make sure the 2nd time triggers resolution
    @classmethod
    def have_tables_turned(cls, threshold: int) -> Optional[str]:
        rev_count = cls.revolution_count()
        peace_count = cls.peace_count()

        if rev_count > peace_count:
            if rev_count >= threshold:
                return "revolution"
        if peace_count > rev_count:
            if peace_count >= threshold:
                return "peace"

        return None

    @classmethod
    def vote_count(cls) -> int:
        return len(cls.db().all())

    @classmethod
    def revolution_count(cls) -> int:
        return len(cls.revolutionaries())

    @classmethod
    def peace_count(cls) -> int:
        return len(cls.peace_keepers())

    def vote(self, vote: str) -> Dict["str", int]:
        user = self._find_user()

        def user_vote(new_vote: str) -> Callable[[Dict], None]:
            def transform(doc: Dict) -> None:
                doc["vote"] = new_vote

            return transform

        if user:
            print(f"Previous Vote for User {self.user}!")
            self.db().update(user_vote(vote), Query().user == self.user)
        else:
            warning(f"NO Previous Vote for User {self.user}!")

            self._vote = vote
            with transaction(self.db()) as tr:
                tr.insert(self.doc())

        return {"Revolution": self.revolution_count(), "Peace": self.peace_count()}

    def _find_user(self) -> Optional[Dict]:
        user = self.db().search(Query().user == self.user)

        if user:
            return user[-1]
        else:
            return None
