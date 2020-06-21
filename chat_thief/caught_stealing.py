from random import random

from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest

# jr_boss: But then make the change of getting "caught" while stealing 50%

# artmattdank: unless they are in the thieves guild?!?

# zanuss: After coup you're not a thief anymore

# eitanfuturo: @zanuss maybe you stop being a thief only if revolution wins?

# zanuss: Do we de-register a thieves vote if they have voted before they get caught?

# baldclap: if youre casught you dont get sound either

# awfulwaffl3: thief if caught they lose cool points, and if they don't have
# enough to cover the cool point loss, they go negative
# zanuss: Maybe there is bail costs and it increases everytime you get caught
# cachesking: negative? that's interesting. we'd have to submit sounds to pay our debt
# bopojoe_: is the thief chance based on street Cred
# cachesking: negative? that's interesting. we'd have to submit sounds to pay our debt
# bopojoe_: more streetCret less chance of being classed as thief
# awfulwaffl3: if you're a thief and get caught. you should be able to RNG to the
# bot to pay sound as debt
# 10sec or so, he catches the thief

# Citizen arrest!

# How do I increase my stealth???

# jr_boss: Or make it so that when someone uses !steal, a random active chatter
# gets called as a policeman by beginbotbot and when he types !arrest within like

# Potential Punishments:
#   - Mark you as thief

# unlucksmcgee: Perhaps percentage is different based on the user you're stealing from. A rich user has more wealth so more security? A rich thief has more wealth to be more stealthy?
# unlucksmcgee: Use GANs to generate artificial faces for the wanted posters using the username as a seed
# unlucksmcgee: Perhaps make the random number 0.7 dynamic based on number of recent steals (similar to the police being on high alert from a recent steal

from chat_thief.models.rap_sheet import RapSheet
from chat_thief.models.user import User


# In the future activities in our economy should affect this numer
# If a Revolution was crushed, Stealing should be very
# It kinda implies police state
DEFAULT_CHANCE_OF_GETTING_CAUGHT = 0.7


class CaughtStealing:
    def __init__(self, thief, target_sfx, victim):
        self.thief = thief
        self.target_sfx = target_sfx
        self.victim = victim

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

                # chance_of_getting_of_caught = (
                #     (chance_of_getting_of_caught * 100) - wealth_disparity
                # ) / 100
            else:
                wealth_diff = victim_wealth / thief_wealth
                if wealth_diff > 100:
                    chance_of_getting_of_caught = 0.99
                elif wealth_diff > 50:
                    chance_of_getting_of_caught = 0.95
                else:
                    chance_of_getting_of_caught = 0.90

        print(f"CHANCE OF Getting Caught: {chance_of_getting_of_caught}")
        busted = random() < chance_of_getting_of_caught

        if busted:
            print("Caught Stealing!!!")
            PlaySoundeffectRequest(user="beginbotbot", command="nope").save()
            User(self.thief).set_value("mana", 0)
            RapSheet(
                user=self.thief,
                action="caught_stealing",
                metadata={"target_sfx": self.target_sfx, "victim": self.victim},
            ).save()
        else:
            print("YOU GOT AWAY WITH STEALING!!!")
            PlaySoundeffectRequest(user="beginbotbot", command="yoink").save()

        return busted, chance_of_getting_of_caught
