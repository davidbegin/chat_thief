from random import random

from chat_thief.bwia import BWIA
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.rap_sheet import RapSheet
from chat_thief.models.user import User


DEFAULT_CHANCE_OF_GETTING_CAUGHT = 0.7


class CaughtStealing:
    def __init__(self, thief, target_sfx, victim, steal_count=0):
        self.thief = thief
        self.target_sfx = target_sfx
        self.victim = victim
        self.steal_count = steal_count

    def call(self) -> bool:
        thief_wealth = User(self.thief).wealth()
        victim_wealth = User(self.victim).wealth()
        chance_of_getting_of_caught = DEFAULT_CHANCE_OF_GETTING_CAUGHT

        print(f"victim_wealth: {victim_wealth}")
        print(f"thief_wealth: {thief_wealth}")

        if thief_wealth > 1:
            wealth_disparity = victim_wealth / thief_wealth
            victim_is_rich = wealth_disparity > 1
            print(f"wealth_disparity: {wealth_disparity}")

            if victim_is_rich:
                wealth_diff = thief_wealth / victim_wealth

                if wealth_diff > 100:
                    chance_of_getting_of_caught = 0.40
                elif wealth_diff > 50:
                    chance_of_getting_of_caught = 0.50
                else:
                    chance_of_getting_of_caught = 0.60
            else:
                wealth_diff = victim_wealth / thief_wealth
                if wealth_diff > 100:
                    chance_of_getting_of_caught = 0.99
                elif wealth_diff > 50:
                    chance_of_getting_of_caught = 0.95
                else:
                    chance_of_getting_of_caught = 0.90

        # Around a 5% increase in getting caught per steal
        chance_of_getting_of_caught += self.steal_count / 20
        print(f"CHANCE OF Getting Caught: {chance_of_getting_of_caught}")
        busted = random() < chance_of_getting_of_caught

        if busted:
            print("Caught Stealing!!!")
            # PlaySoundeffectRequest(user="beginbotbot", command="nope").save()
            User(self.thief).set_value("mana", 0)
            RapSheet(
                user=self.thief,
                action="caught_stealing",
                metadata={"target_sfx": self.target_sfx, "victim": self.victim},
            ).save()
        else:
            print("YOU GOT AWAY WITH STEALING!!!")
            # PlaySoundeffectRequest(user="beginbotbot", command="yoink").save()

        return busted, chance_of_getting_of_caught
