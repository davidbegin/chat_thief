from typing import List, Tuple, Any, Callable, Dict

from chat_thief.models.database import db_table
from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.user import User
from chat_thief.config.log import error, warning, success
from chat_thief.models.transaction import transaction

from tinydb import Query  # type: ignore

DEFAULT_VOTES_DB_PATH = "db/cube_bets.json"

# TODO: Maybe this should be Bets
Bet = Tuple[str, int, List[str]]


class CubeBet(BaseDbModel):
    table_name = "cube_bets"
    database_path = "db/cube_bets.json"

    def __init__(self, user: str, duration: int, wager: List[str] = []):
        self._user = user
        self._duration = int(duration)
        self._wager = wager

    def doc(self) -> Dict:
        return {"user": self._user, "duration": self._duration, "wager": self._wager}

    def save(self) -> "CubeBet":
        bet = self.db().get(Query().user == self._user)

        if bet:
            self.set_value("duration", self._duration)
        else:
            success(f"Creating New Cube Bet: {self.doc()}")

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
        return self

    def duration(self) -> int:
        return self.cube_bet()["duration"]

    def user(self) -> str:
        return self.cube_bet()["user"]

    @property
    def wager(self) -> List[str]:
        return self.cube_bet()["wager"]

    # TODO: Combine these methods
    def cube_bet(self) -> Dict:
        return self._find_or_create_cube_bet()

    def _find_or_create_cube_bet(self) -> Dict:
        result = self.db().get(Query().user == self._user)

        if result:
            return result

        success(f"Creating New Cube Bet: {self.doc()}")

        with transaction(self.db()) as tr:
            tr.insert(self.doc())
        return self.doc()

    def create_or_update(self) -> Dict:
        result = self.db().get(Query().user == self._user)

        if result:
            success(f"Updating Cube Bet: {self.doc()}")
            self.db().update(self.doc(), doc_ids=[result.doc_id])
        else:
            success(f"Creating New Cube Bet: {self.doc()}")

            with transaction(self.db()) as tr:
                tr.insert(self.doc())

        return self.doc()

    def set_value(self, field: str, value: Any) -> None:
        def _update_that_value() -> Callable[[Dict], None]:
            def transform(doc: Dict) -> None:
                doc[field] = value

            return transform

        with transaction(self.db()) as tr:
            tr.update(_update_that_value(), Query().user == self._user)

    # TODO: Maybe this should be bets
    @classmethod
    def all_bets(cls) -> List[Bet]:
        bets = [(bet["user"], bet["duration"], bet["wager"]) for bet in cls.db().all()]
        return sorted(bets, key=lambda bet: bet[1])
