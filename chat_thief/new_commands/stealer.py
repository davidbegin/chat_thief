from chat_thief.new_commands.result import Result
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.caught_stealing import CaughtStealing


class Stealer:
    def __init__(self, thief, target_sfx, victim):
        self._thief = thief
        self._target_sfx = target_sfx
        self._victim = victim
        self.metadata = {"victim": self._victim, "target_sfx": self._target_sfx}

    def steal(self):
        command = Command(self._target_sfx)
        thief = User(self._thief)
        cool_points = thief.cool_points()

        if self._target_sfx not in User(self._victim).commands():
            self.metadata[
                "stealing_result"
            ] = f"!{self._target_sfx} is not owned by @{self._victim}"
        elif cool_points >= command.cost():

            was_caught_stealing = CaughtStealing(
                self._thief, self._target_sfx, self._victim
            ).call()

            if was_caught_stealing:
                self.metadata[
                    "stealing_result"
                ] = f"@{self._thief} WAS CAUGHT STEALING!"
            else:
                self._steal(command, thief)
        else:
            self.metadata["stealing_result"] = f"@{self._thief} BROKE BOI!"

        return Result(user=self._thief, command="steal", metadata=self.metadata)

    def _steal(self, command, thief):
        thief.update_cool_points(-command.cost())
        command.allow_user(self._thief)
        command.unallow_user(self._victim)
        command.increase_cost(command.cost() * 2)
        self.metadata["stealing_result"] = f"@{self._thief} stole from @{self._victim}"
