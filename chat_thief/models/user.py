from typing import List, Dict, Tuple, Optional, Any, Iterator

from tinydb import Query  # type: ignore

from chat_thief.models.database import db_table  # type: ignore
from chat_thief.prize_dropper import random_soundeffect  # type: ignore
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary  # type: ignore
from chat_thief.config.log import error, warning, success  # type: ignore
from chat_thief.models.command import Command  # type: ignore
from chat_thief.models.base_db_model import BaseDbModel  # type: ignore
from chat_thief.models.transaction import transaction  # type: ignore


class User(BaseDbModel):
    table_name = "users"
    database_path = "db/users.json"

    def __init__(
        self,
        name: str,
        cool_points: int = 0,
        top_eight: List[str] = [],
        custom_css: Optional[str] = None,
        insured: Optional[bool] = False,
    ):
        self._top_eight = top_eight
        self.name = name
        self._cool_points = cool_points
        self._custom_css = custom_css
        self._insured = insured
        self._raw_user = self._find_or_create_user()

    @classmethod
    def register_bot(cls, bot: str, creator: str) -> None:
        cls.db().upsert(
            {"is_bot": True, "creator": creator, "name": bot}, Query().name == bot
        )

    @classmethod
    def bots(cls) -> List[str]:
        return [bot["name"] for bot in cls.db().search(Query().is_bot == True)]

    @classmethod
    def total_street_cred(cls) -> int:
        return cls._total_of_field("street_cred")

    @classmethod
    def total_cool_points(cls) -> int:
        return cls._total_of_field("cool_points")

    @classmethod
    def _total_of_field(cls, field: str) -> int:
        return sum([user[field] for user in cls.db().all()])

    @classmethod
    def richest_cool_points(cls) -> List[Dict]:
        return cls.max_of_field("cool_points")

    @classmethod
    def max_of_field(cls, field: str) -> List[Dict]:
        users = [user for user in cls.db().all()]

        if users:
            # TODO: This ain't right
            return sorted(users, key=lambda user: user.get(field, 0))[-1]
        else:
            return []

    @classmethod
    def by_cool_points(cls) -> List[Dict]:
        users = [user for user in cls.db().all()]
        if users:
            return list(reversed(sorted(users, key=lambda user: user["cool_points"])))
        else:
            return []

    @classmethod
    def richest(cls) -> List[Tuple[str, int]]:
        users = [(user["name"], user["cool_points"]) for user in cls.db().all()]
        return sorted(users, key=lambda user: user[1])

    # ====================================================================

    # So this means, when we call, we find or init, thats fine!
    def user(self) -> Dict:
        return self._find_or_create_user()

    def stats(self) -> str:
        return (
            f"@{self.name} - Mana: {self.mana()} | "
            f"Street Cred: {self.street_cred()} | "
            f"Cool Points: {self.cool_points()} | "
            f"Wealth: {self.wealth()} | "
            f"Insured: {self.insured()}"
        )

    def commands(self) -> List[str]:
        return [
            permission["name"]
            for permission in Command.for_user(self.name)
            if permission["name"] != self.name
        ]

    # Seems like it should be factored away
    def street_cred(self) -> int:
        return self._fetch_field("street_cred", 0)

    def cool_points(self) -> int:
        return self._fetch_field("cool_points", 0)

    def custom_css(self) -> Optional[str]:
        return self._fetch_field("custom_css", None)

    def mana(self) -> int:
        return self._fetch_field("mana", 0)

    def is_bot(self) -> bool:
        return self._fetch_field("is_bot", False)

    def creator(self) -> Optional[str]:
        return self._fetch_field("creator", None)

    def top_eight(self) -> List[str]:
        return self._fetch_field("top_eight", [])

    def insured(self) -> bool:
        return self._fetch_field("insured", False)

    def _fetch_field(self, field: str, default: Any) -> Any:
        return self.user().get(field, default)

    # =============================================

    def update_mana(self, amount: int) -> None:
        self.update_value("mana", amount)

    # The ride or dies you have
    def karma(self) -> int:
        user_result = self.db().search(Query().ride_or_die == self.name)
        return len(user_result)

    def kill(self) -> None:
        self.update_value("mana", -self.mana())

    def revive(self, mana: int = 3) -> None:
        self.set_value("mana", mana)

    def paperup(self, amount: int = 100) -> str:
        self.update_street_cred(amount)
        self.update_cool_points(amount)
        return f"@{self.name} has been Papered Up"

    def doc(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "custom_css": self._custom_css,
            "street_cred": 0,
            "cool_points": self._cool_points,
            "mana": 3,
            "top_eight": self._top_eight,
            "insured": self._insured,
        }

    # This also might need a quick exit
    # This Might be potentially a problem
    def _find_affordable_random_command(self) -> Command:
        if self.cool_points() < 1:
            raise ValueError("You can't afford anything!")

        looking_for_effect = True

        while looking_for_effect:
            effect = random_soundeffect()
            command = Command(effect)
            if self.cool_points() >= command.cost() and not command.allowed_to_play(
                self.name
            ):
                looking_for_effect = False
        return command

    # This is going to reveal some bugs
    # or bad code
    #  returning just a Dict
    # or a Result from Query, which is a fancy dictionary
    def _find_or_create_user(self) -> Dict:
        user_result = self.db().get(Query().name == self.name)
        if user_result:
            return user_result
        else:
            success(f"Creating New User: {self.doc()}")

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def update_cool_points(self, amount: int = 1) -> None:
        return self.update_value("cool_points", amount)

    def update_street_cred(self, amount: int = 1) -> None:
        self.update_value("street_cred", amount)

    def clear_top_eight(self) -> None:
        self.set_value("top_eight", [])

    def set_ride_or_die(self, ride_or_die: str) -> None:
        if ride_or_die != self.name:
            self.set_value("ride_or_die", ride_or_die)

    def add_to_top_eight(self, friend: str) -> None:
        current_eight = self.top_eight()

        if len(current_eight) == 8:
            raise ValueError("You can only have 8 in your Top 8!")

        if friend not in current_eight and len(current_eight) < 8:
            current_eight.append(friend)
            self.set_value("top_eight", current_eight)

    def remove_from_top_eight(self, enemy: str) -> None:
        current_eight = self.top_eight()
        if enemy in current_eight:
            current_eight.remove(enemy)
            self.set_value("top_eight", current_eight)

    def top_wealth(self) -> int:
        user_data = self.user()
        user_commands = Command.for_user(self.name)
        total_command_wealth = sum([command["cost"] for command in user_commands])
        return user_data["cool_points"] + total_command_wealth

    @classmethod
    def wealthiest(cls) -> Tuple[str, int]:
        richest = [
            (user["name"], User(user["name"]).top_wealth()) for user in cls.db().all()
        ]
        return sorted(richest, key=lambda user: user[1])[-1][0]

    def remove_all_commands(self) -> None:
        for command in self.commands():
            Command(command).unallow_user(self.name)

    def bankrupt(self) -> str:
        self.update_street_cred(-self.street_cred())
        self.update_cool_points(-self.cool_points())
        return f"@{self.name} is now Bankrupt"

    def wealth(self) -> int:
        return (
            sum([Command(command).cost() for command in self.commands()])
            + self.cool_points()
        )

    def buy_insurance(self) -> str:
        current_cool_points = self.cool_points()
        if current_cool_points > 0:
            cool_points = current_cool_points - 1
            self.db().upsert(
                {"cool_points": cool_points, "insured": True}, Query().name == self.name
            )
            return f"@{self.name} thank you for purchasing insurance"
        else:
            return f"YA Broke @{self.name} - it costs 1 Cool Point to buy insurance"
