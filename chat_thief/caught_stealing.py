from random import randint
from typing import Tuple

from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.rap_sheet import RapSheet
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.utils.stats import clamp


# Your chance of stealing starts at 50%
DEFAULT_CHANCE = 50

# How much you increase your chances
# from stealing or giving
SOCIETY_BONUS_MULTIPLIER = 5
MAX_SOCIETY_BONUS = 20
MIN_SOCIETY_PUNISHMENT = -50

# How much you can increase your chances of stealing
# based on the wealth disparity between thief and victim
WEALTH_DISPARITY_MULTIPLER = 1
MAX_WEALTH_DISPARITY_BONUS = 20
MAX_WEALTH_DISPARITY_PUNISHMENT = -20

# If a command is over an amount it's harder to steal
EXPENSIVE_COMMAND_COST_LIMIT = 100
EXPENSIVE_COMMAND_PUNISHMENT = -10


class CaughtStealing:
    def __init__(self, thief, target_sfx, victim, steal_count=0, give_count=0):
        self.thief = thief
        self.target_sfx = target_sfx

        self.victim = victim
        self.steal_count = steal_count
        self.give_count = give_count

        self.target_sfx_cost = Command(target_sfx).cost()
        self.thief_wealth = User(self.thief).wealth()
        self.victim_wealth = User(self.victim).wealth()

    def call(self) -> Tuple[bool, int]:
        success_range = self._calc_chance_of_success()
        roll_of_the_dice = randint(0, 100)
        busted = roll_of_the_dice > success_range

        if busted:
            print("Caught Stealing!!!")
            # if self.steal_count < 1:
            #     PlaySoundeffectRequest(user="beginbotbot", command="nope").save()
            User(self.thief).set_value("mana", 0)
            RapSheet(
                user=self.thief,
                action="caught_stealing",
                metadata={"target_sfx": self.target_sfx, "victim": self.victim},
            ).save()
        else:
            print("YOU GOT AWAY WITH STEALING!!!")
            if self.target_sfx_cost > EXPENSIVE_COMMAND_COST_LIMIT:
                PlaySoundeffectRequest(user="beginbotbot", command="yoink").save()

        return busted, success_range

    # Chance of Succeeding From: 0 ... 100
    def _calc_chance_of_success(self) -> int:
        chance = DEFAULT_CHANCE
        chance = self._society_bonus(chance)
        chance = self._wealth_disparity_bonus(chance)
        chance = self._target_cost_bonus(chance)
        return chance

    # For Every Steal or Give you lose or gain some chance
    def _society_bonus(self, chance):
        society_factor = (self.give_count - self.steal_count) * SOCIETY_BONUS_MULTIPLIER
        society_factor = clamp(
            society_factor, MIN_SOCIETY_PUNISHMENT, MAX_SOCIETY_BONUS
        )
        return chance + society_factor

    # Wealth disparity can affect you chance of a successful steal
    def _wealth_disparity_bonus(self, chance):
        wealth_disparity = (
            int(self.victim_wealth / max(self.thief_wealth, 1))
            * WEALTH_DISPARITY_MULTIPLER
        )
        wealth_disparity = clamp(
            wealth_disparity,
            MAX_WEALTH_DISPARITY_PUNISHMENT,
            MAX_WEALTH_DISPARITY_BONUS,
        )
        return chance - wealth_disparity

    # If a command is over an amount it's harder to steal
    def _target_cost_bonus(self, chance):
        if self.target_sfx_cost > EXPENSIVE_COMMAND_COST_LIMIT:
            return chance - EXPENSIVE_COMMAND_PUNISHMENT
        return chance
