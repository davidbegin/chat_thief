from chat_thief.new_commands.result import Result
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.caught_stealing import CaughtStealing
from chat_thief.bwia import BWIA


class Stealer:
    def __init__(self, thief, target_sfx, victim):
        self._thief = thief
        self._target_sfx = target_sfx
        self._victim = victim
        self.metadata = {"victim": self._victim, "target_sfx": self._target_sfx}

    def steal(self):
        command = Command(self._target_sfx)
        thief = User(self._thief)
        the_odds = 0.7

        if thief.mana() < 3:
            self.metadata[
                "stealing_result"
            ] = f"@{self._thief} has no Mana to steal from @{self._victim}"
        elif self._target_sfx not in User(self._victim).commands():
            self.metadata[
                "stealing_result"
            ] = f"!{self._target_sfx} is not owned by @{self._victim}"
        else:
            self._attempt_robbery(thief, command)

        return Result(user=self._thief, command="steal", metadata=self.metadata)

    def _attempt_robbery(self, thief, command):
        thief.update_mana(-2)
        steal_count = BWIA.find_thief(thief)
        give_count = BWIA.robinhood_score(thief)

        print(f"This Thief Has Stolen {steal_count} times before")
        was_caught_stealing, the_odds = CaughtStealing(
            self._thief, self._target_sfx, self._victim, steal_count, give_count
        ).call()
        the_odds = f"{the_odds}%"
        victim = User(self._victim)

        if victim.insured():
            victim.set_value("insured", False)
            self.metadata[
                "stealing_result"
            ] = f"@{self._thief} was blocked by @{self._victim}'s insurance! Num Attempts: {steal_count}"
        elif was_caught_stealing:
            thief.update_value("notoriety", 1)
            self.metadata[
                "stealing_result"
            ] = f"@{self._thief} WAS CAUGHT STEALING! Chance of Success: {the_odds}. Num Attempts: {steal_count}"
            User(self._thief).set_value("mana", 0)
        else:
            self._steal(command, thief, the_odds)

    def _steal(self, command, thief, the_odds):
        command.allow_user(self._thief)
        command.unallow_user(self._victim)
        command.increase_cost(command.cost())
        self.metadata[
            "stealing_result"
        ] = f"@{self._thief} stole from @{self._victim}. Chance of Success: {the_odds}"
