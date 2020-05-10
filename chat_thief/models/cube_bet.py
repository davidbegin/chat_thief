DEFAULT_VOTES_DB_PATH = "db/cube_bets.json"

from chat_thief.models.database import db_table
from chat_thief.models.base_model import BaseModel
from chat_thief.models.user import User
from chat_thief.config.log import error, warning, success
from tinydb import Query


class CubeBet(BaseModel):
    table_name = "cube_bets"
    database_folder = ""
    database_path = "db/cube_bets.json"

    @classmethod
    def purge(cls):
        return cls.db().purge()

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    @classmethod
    def all_bets(cls):
        bets = [(bet["name"], bet["duration"]) for bet in cls.db().all()]
        return sorted(bets, key=lambda bet: bet[1])

    def __init__(self, name, duration):
        self.name = name
        self._duration = int(duration)

    def save(self):
        bet = self.db().get(Query().name == self.name)

        if bet:
            self._set_value("duration", self._duration)
        else:
            success(f"Creating New Cube Bet: {self.doc()}")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
        return self.doc()

    def duration(self):
        return self.cube_bet()["duration"]

    def name(self):
        return self.cube_bet()["name"]

    def cube_bet(self):
        return self._find_or_create_cube_bet()

    def _find_or_create_cube_bet(self):
        result = self.db().get(Query().name == self.name)

        if result:
            return result

        success(f"Creating New Cube Bet: {self.doc()}")
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(self.doc())
        return self.doc()

    def doc(self):
        return {"name": self.name, "duration": self._duration}
