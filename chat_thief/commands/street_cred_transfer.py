from chat_thief.models.user import User


class StreetCredTransfer:
    def __init__(self, user, cool_person, amount=1):
        self.user = user
        self.cool_person = cool_person
        self.amount = amount

        if self.user == self.cool_person:
            raise ValueError(f"Can't give yourself Cool Points @{self.user}!")

    def transfer(self):
        transferrer = User(self.user)

        if transferrer.street_cred() >= self.amount:
            transferrer.update_street_cred(-self.amount)

            transferree = User(self.cool_person)
            transferree.update_cool_points(self.amount)
            return f"@{self.user} gave {self.amount} Street Cred to @{self.cool_person}"
        else:
            return f"@{self.user} NOT ENOUGH STREET CRED!"
