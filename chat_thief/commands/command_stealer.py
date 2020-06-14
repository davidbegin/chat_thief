from chat_thief.models.command import Command
from chat_thief.models.user import User


class CommandStealer:
    def __init__(self, thief, victim, command):
        self.thief = thief
        self.victim = victim
        self.command = command

    def steal(self):
        command = Command(self.command)
        user = User(self.thief)

        if command.name not in User(self.victim).commands():
            f"{command.name} is not owned by {user.name}"

        cool_points = user.cool_points()

        if cool_points >= command.cost():
            user.update_cool_points(-command.cost())
            command.allow_user(self.thief)
            command.unallow_user(self.victim)
            command.increase_cost(command.cost() * 2)
            return f"@{self.thief} stole from @{self.victim}"
        else:
            return f"@{self.thief} BROKE BOI!"
