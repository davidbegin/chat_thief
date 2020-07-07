import traceback
import os
from collections import Counter

from typing import Dict, List, Tuple, Any, Optional, Callable
from itertools import chain

from tinydb import Query  # type: ignore

from chat_thief.config.log import success, warning, error
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.database import db_table
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.models.transaction import transaction


class Command(BaseDbModel):
    table_name = "commands"
    database_path = "db/commands.json"

    def __init__(self, name: str, inital_cost: int = 1):
        self.name = name
        self.permitted_users: List[str] = []
        self.inital_health = 3
        self.inital_cost = inital_cost
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()

    def doc(self) -> Dict:
        return {
            "name": self.name,
            "user": "beginbot",
            "permitted_users": self.permitted_users,
            "health": self.inital_health,
            "cost": self.inital_cost,
        }

    def command(self) -> Dict:
        if command_result := self.db().search(Query().name == self.name):
            return command_result[0]
        else:
            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def health(self) -> int:
        return self._fetch_field("health", 0)

    def cost(self) -> int:
        return self._fetch_field("cost", 1)

    def users(self) -> List[str]:
        return self._fetch_field("permitted_users", [])

    @classmethod
    def available_sounds(cls) -> Optional[List[Dict]]:
        def test_func(val: List[str]) -> bool:
            return len(val) > 0

        return cls.db().search(Query().permitted_users.test(test_func))

    @classmethod
    def most_expensive(cls) -> Optional[Dict]:
        if cmd_by_cost := cls.by_cost():
            return cmd_by_cost[0]
        else:
            return None

    @classmethod
    def by_cost(cls) -> List[Dict]:
        cmds = cls.db().all()
        if cmds:
            return list(reversed(sorted(cmds, key=lambda cmd: cmd["cost"])))
        else:
            return []

    # Incompatible return value type (got "Iterator[Any]", expected "List[Dict[Any, Any]]")
    # These are subtly different
    # one time, we return the search
    # other time, we save and return result of the save
    @classmethod
    def find_or_create(cls, name: str) -> Dict:
        found_command = cls.db().get(Query().name == name)

        if found_command:
            return found_command
        else:
            new_command = cls(name)
            new_command.save()
            return new_command.doc()

    @classmethod
    def for_user(cls, user: str) -> List[Dict]:
        def in_permitted_users(permitted_users: List[str], current_user: str) -> bool:
            return current_user in permitted_users

        return [
            permission
            for permission in cls.db().search(
                Query().permitted_users.test(in_permitted_users, user)
            )
        ]

    @classmethod
    def most_popular(cls) -> List[str]:
        result = cls.db().all()
        sorted_commands = sorted(result, key=lambda command: command["cost"])
        return [
            f"{command['name']}: {command['cost']}" for command in sorted_commands[-5:]
        ]

    def exists(self) -> bool:
        return self.db().get(Query().name == self.name) is not None

    def allowed_to_play(self, user: str) -> bool:
        if self.is_theme_song:
            return user == self.name

        if user in STREAM_GODS:
            return True

        if command := self.db().get(Query().name == self.name):
            return user in command["permitted_users"]

        return False

    def update_health(self, amount: int) -> None:
        self.update_value("health", amount)

    def revive(self) -> None:
        self.set_value("health", 3)

    def silence(self) -> None:
        self.set_value("health", 0)

    def increase_cost(self, amount: int = 1) -> None:
        if command := self.db().get(Query().name == self.name):
            self.update_value("cost", amount)

    # TODO: Figure if this throwing ValueError's often
    def unallow_user(self, target_user: str) -> Optional[str]:
        try:
            command = self.db().get(Query().name == self.name)
            if command:
                self._remove_user(target_user)
                return f"@{target_user} lost access to !{self.name}"
            else:
                return f"No One has accesss to !{self.name}"
        except ValueError as e:
            traceback.print_exc()
            return f"Error Unallowing User: {e}"

    def allow_user(self, target_user: str) -> str:
        command = self.db().get(Query().name == self.name)

        # What if we are none
        if command:
            if target_user not in command["permitted_users"]:
                self._add_user(target_user)
                return f"@{target_user} now has access to !{self.name}"
            else:
                return f"@{target_user} already allowed !{self.name}"
        else:
            self.permitted_users = [target_user]
            self.save()
            return f"@{target_user} is the 1st person with access to: !{self.name}"

    def decay(self) -> None:
        current_cost = self.cost()
        if current_cost > 1:
            current_cost - 1
            self.set_value("cost", current_cost - 1)

    def _add_user(self, target_user: str) -> None:
        def add_permitted_users() -> Callable[[Dict], None]:
            def transform(doc: Dict) -> None:
                doc["permitted_users"].append(target_user)

            return transform

        self.update(add_permitted_users)

    def _remove_user(self, target_user: str) -> None:
        def remove_permitted_users() -> Callable[[Dict], None]:
            def transform(doc: Dict) -> None:
                if target_user in doc["permitted_users"]:
                    doc["permitted_users"].remove(target_user)

            return transform

        self.update(remove_permitted_users)

    def _fetch_field(self, field: str, default: Any) -> Any:
        return self.command().get(field, default)
