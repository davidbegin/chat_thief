DEFAULT_VOTES_DB_PATH = "db/cube_bets.json"

from chat_thief.models.database import db_table
from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.user import User
from chat_thief.config.log import error, warning, success
from tinydb import Query  # type: ignore

from chat_thief.models.transaction import transaction


class CubeBet(BaseDbModel):
    table_name = "cube_bets"
    database_path = "db/cube_bets.json"

    @classmethod
    def all_bets(cls):
        bets = [(bet["user"], bet["duration"], bet["wager"]) for bet in cls.db().all()]
        return sorted(bets, key=lambda bet: bet[1])

    def __init__(self, user, duration, wager=[]):
        self.user = user
        self._duration = int(duration)
        self._wager = wager

    def save(self):
        bet = self.db().get(Query().user == self.user)

        if bet:
            self.set_value("duration", self._duration)
        else:
            success(f"Creating New Cube Bet: {self.doc()}")

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
        return self.doc()

    def duration(self):
        return self.cube_bet()["duration"]

    def user(self):
        return self.cube_bet()["user"]

    def wager(self):
        return self.cube_bet()["wager"]

    def cube_bet(self):
        return self._find_or_create_cube_bet()

    def create_or_update(self):
        result = self.db().get(Query().user == self.user)

        if result:
            success(f"Updating Cube Bet: {self.doc()}")
            result = self.db().update(self.doc(), doc_ids=[result.doc_id])
            return result
        else:
            success(f"Creating New Cube Bet: {self.doc()}")

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def _find_or_create_cube_bet(self):
        result = self.db().get(Query().user == self.user)

        if result:
            return result

        success(f"Creating New Cube Bet: {self.doc()}")

        with transaction(self.db()) as tr:
            tr.insert(self.doc())
        return self.doc()

    def doc(self):
        return {"user": self.user, "duration": self._duration, "wager": self._wager}

    def set_value(self, field, value):
        def _update_that_value():
            def transform(doc):
                doc[field] = value

            return transform

        with transaction(self.db()) as tr:
            tr.update(_update_that_value(), Query().user == self.user)
