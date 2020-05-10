DEFAULT_VOTES_DB_PATH = "db/cube_bets.json"

from chat_thief.models.database import db_table
from chat_thief.models.user import User
from chat_thief.config.log import error, warning, success
from tinydb import Query


class CubeBet:
    table_name = "cube_bets"
    database_folder = ""
    database_path = "db/cube_bets.json"

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def __init__(self, gambler, duration):
        self.gambler = gambler
        self.duration = int(duration)

    def save(self):
        return self._find_or_create_cube_bet()

    def _find_or_create_cube_bet(self):
        result = self.db().get(Query().gambler == self.gambler)

        if result:
            return result

        success(f"Creating New Cube Bet: {self.doc()}")
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(self.doc())
        return self.doc()

    def doc(self):
        return {"gambler": self.gambler, "duration": self.duration}
