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

        if thief.mana() < 1:
            self.metadata[
                "stealing_result"
            ] = f"@{self._thief} has no Mana to steal from @{self._victim}"
        elif self._target_sfx not in User(self._victim).commands():
            self.metadata[
                "stealing_result"
            ] = f"!{self._target_sfx} is not owned by @{self._victim}"
        else:
            thief.update_mana(-1)
            was_caught_stealing = CaughtStealing(
                self._thief, self._target_sfx, self._victim
            ).call()

            if was_caught_stealing:
                self.metadata[
                    "stealing_result"
                ] = f"@{self._thief} WAS CAUGHT STEALING!"
                User(self._thief).set_value("mana", 0)
            else:
                self._steal(command, thief)

        return Result(user=self._thief, command="steal", metadata=self.metadata)

    def _steal(self, command, thief):
        command.allow_user(self._thief)
        command.unallow_user(self._victim)
        command.increase_cost(command.cost())
        self.metadata["stealing_result"] = f"@{self._thief} stole from @{self._victim}"
