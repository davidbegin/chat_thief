import random

from chat_thief.soundeffects_library import SoundeffectsLibrary


def random_soundeffect(self):
    return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]


# Not include STREAM LORDS
def random_user(self):
    return random.sample(WelcomeCommittee.fetch_present_users(), 1)[0]


def drop_soundeffect(self):
    user = self.random_user()
    soundeffect = self.random_soundeffect()
    soundeffect_name = CommandPermissionCenter().add_permission_for_user(
        user, soundeffect_name
    )
    msg = f"@{user} now has access to Sound Effect: !{soundeffect_name}"
    return msg
