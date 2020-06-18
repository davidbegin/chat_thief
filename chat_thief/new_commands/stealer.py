from chat_thief.new_commands.result import Result
from chat_thief.models.user import User
from chat_thief.models.command import Command


class Stealer:
    def __init__(self, thief, target_sfx, victim):
        self._thief = thief
        self._target_sfx = target_sfx
        self._victim = victim
        self.metadata = {"victim": self._victim, "target_sfx": self._target_sfx}

    def steal(self):
        command = Command(self._target_sfx)
        thief = User(self._thief)

        if command.name not in User(self._victim).commands():
            f"{command.name} is not owned by {thief.name}"

        cool_points = thief.cool_points()

        if cool_points >= command.cost():
            thief.update_cool_points(-command.cost())
            command.allow_user(self._thief)
            command.unallow_user(self._victim)
            command.increase_cost(command.cost() * 2)
            self.metadata[
                "stealing_result"
            ] = f"@{self._thief} stole from @{self._victim}"
        else:
            self.metadata["stealing_result"] = f"@{self._thief} BROKE BOI!"

        return Result(user=self._thief, command="steal", metadata=self.metadata)
