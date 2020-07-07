from typing import List, Dict, Callable, Any

from tinydb import Query  # type: ignore

from chat_thief.models.database import db_table
from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.transaction import transaction


class SFXVote(BaseDbModel):
    table_name = "sfx_votes"
    database_path = "db/sfx_votes.json"

    # Incompatible default for argument "detractors" (default has type
    # "Type[List[Any]]", argument has type "List[Any]")
    def __init__(
        self, command: str, supporters: List[Any] = [], detractors: List[Any] = []
    ):
        self.command = command
        self.supporters = supporters
        self.detractors = detractors

    def doc(self) -> Dict:
        return {
            "command": self.command,
            "supporters": self.supporters,
            "detractors": self.detractors,
        }

    def support(self, supporter: str) -> Dict:
        vote = self._find_or_create_vote()

        def show_support(supporter: str) -> Callable[[Dict], None]:
            def transform(doc: Dict) -> None:
                if supporter not in doc["supporters"]:
                    doc["supporters"].append(supporter)
                if supporter in doc["detractors"]:
                    doc["detractors"].remove(supporter)

            return transform

        self.db().update(show_support(supporter), Query().command == self.command)
        return self._find_or_create_vote()

    def detract(self, detractor: str) -> Dict:
        vote = self._find_or_create_vote()

        def detract_support(detractor: str) -> Callable[[Dict], None]:
            def transform(doc: Dict) -> None:
                if detractor not in doc["detractors"]:
                    doc["detractors"].append(detractor)
                if detractor in doc["supporters"]:
                    doc["supporters"].remove(detractor)

            return transform

        self.db().update(detract_support(detractor), Query().command == self.command)
        return self._find_or_create_vote()

    def like_to_hate_ratio(self) -> float:
        if self.detractor_count() < 1:
            return 100
        total = self.supporter_count() + self.detractor_count()
        return (self.supporter_count() / total) * 100

    def supporter_count(self) -> int:
        vote = self._find_or_create_vote()
        return len(vote["supporters"])

    def detractor_count(self) -> int:
        vote = self._find_or_create_vote()
        return len(vote["detractors"])

    def is_enabled(self) -> bool:
        if self.supporter_count() == 0 and self.detractor_count() == 0:
            return True
        return self.supporter_count() >= self.detractor_count()

    def _find_or_create_vote(self) -> Dict:
        if vote := self.db().get(Query().command == self.command):
            return vote
        else:
            self.save()
            return self.doc()
