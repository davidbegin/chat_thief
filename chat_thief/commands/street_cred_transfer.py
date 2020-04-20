from chat_thief.user import User


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
            transferrer.remove_street_cred()
            transferree = User(self.cool_person)
            transferree.add_cool_points()
            return f"{self.user} gave {self.amount} Street Cred (remaining: {transferrer.street_cred()}) to {self.cool_person}'s total of {transferree.cool_points()} Cool Points"
        else:
            return "NOT ENOUGH STREET CRED!"
