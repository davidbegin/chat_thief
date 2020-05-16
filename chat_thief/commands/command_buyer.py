from chat_thief.models.user import User


class CommandBuyer:
    def __init__(self, user, target_sfx, amount=1):
        self.user = User(user)
        self.target_sfx = target_sfx

    def buy(self):
        if self.target_sfx == "random":
            self.target_sfx = self.user._find_affordable_random_command().name

        return self.user.buy(self.target_sfx)
