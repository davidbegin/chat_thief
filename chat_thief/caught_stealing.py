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

from random import random

from chat_thief.models.rap_sheet import RapSheet
from chat_thief.models.user import User


class CaughtStealing:
    def __init__(self, thief, target_sfx, victim):
        self.thief = thief
        self.target_sfx = target_sfx
        self.victim = victim

    def call(self) -> bool:
        was_caught_stealing = random() < 0.5

        if was_caught_stealing:
            print("Caught Stealing!!!")
            PlaySoundeffectRequest(user="beginbotbot", command="thieves").save()
            User(self.thief).set_value("mana", 0)
            RapSheet(
                user=self.thief,
                action="caught_stealing",
                metadata={"target_sfx": self.target_sfx, "victim": self.victim},
            ).save()
        else:
            print("YOU GOT AWAY WITH STEALING!!!")
            PlaySoundeffectRequest(user="beginbotbot", command="stealing").save()

        return was_caught_stealing
