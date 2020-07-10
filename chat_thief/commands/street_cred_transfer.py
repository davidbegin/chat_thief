from typing import List, Dict, Optional
import random

from chat_thief.models.user import User
from chat_thief.prize_dropper import random_user as find_random_user


class StreetCredTransfer:
    def __init__(
        self, user: str, cool_person: str, top_eight: List[str] = [], amount: int = 1
    ):
        self.user = user
        self.cool_person = cool_person
        self.top_eight = top_eight
        self.amount = amount

        if self.user == self.cool_person:
            raise ValueError(f"Can't give yourself Cool Points @{self.user}!")

    def transfer(self) -> str:
        transferrer = User(self.user)

        if transferrer.street_cred() >= self.amount:
            return self._setup_transfer(transferrer)
        else:
            return f"@{self.user} NOT ENOUGH STREET CRED!"

    def _setup_transfer(self, transferrer: User) -> str:
        if self.cool_person == "random" or self.cool_person is None:
            recipients = []
            for _ in range(0, self.amount):
                cool_person = self._random_user()
                transferree = User(cool_person)
                self._exec_transfer(transferrer, transferree, 1)
                recipients.append(cool_person)

            users = " ".join([f"@{user}" for user in recipients])
            if len(recipients) == 1:
                users_info = users
            else:
                users_info = f"{users} each"
            return f"@{self.user} gave 1 Street Cred to {users_info}"
        else:
            transferree = User(self.cool_person)
            self._exec_transfer(transferrer, transferree, self.amount)
            return f"@{self.user} gave {self.amount} Street Cred to @{transferree.name}"

    def _exec_transfer(self, transferrer: User, transferree: User, amount: int) -> None:
        transferrer.update_street_cred(-amount)
        transferree.update_cool_points(amount)

    def _random_user(self) -> str:
        top_eight = self.top_eight.copy()
        random.shuffle(top_eight)
        return random.sample(top_eight, 1)[0]
