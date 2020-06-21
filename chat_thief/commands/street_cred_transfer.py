from chat_thief.models.user import User
from chat_thief.prize_dropper import random_user as find_random_user


class StreetCredTransfer:
    def __init__(self, user, cool_person, top_eight=[], amount=1):
        self.user = user
        self.cool_person = cool_person
        self.top_eight = top_eight
        self.amount = amount

        if self.user == self.cool_person:
            raise ValueError(f"Can't give yourself Cool Points @{self.user}!")

    def transfer(self):
        transferrer = User(self.user)

        if transferrer.street_cred() >= self.amount:
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
        else:
            return f"@{self.user} NOT ENOUGH STREET CRED!"

    def _exec_transfer(self, transferrer, transferree, amount):
        transferrer.update_street_cred(-amount)
        transferree.update_cool_points(amount)

    def _random_user(self):
        return random.sample(random.shuffle(self.top_eight), 1)[0]
        # self.top_eight
        # return find_random_user(blacklisted_users=[self.user])
