import random

from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS


def random_soundeffect():
    return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]


def random_user():
    looking_for_user = True
    while looking_for_user:
        user = random.sample(WelcomeCommittee.fetch_present_users(), 1)[0]
        if user not in STREAM_LORDS and user != "nightbot":
            looking_for_user = False
    return user


def drop_random_soundeffect_to_random_user():
    user = random_user()
    soundeffect = random_soundeffect()

    soundeffect_name = CommandPermissionCenter(
        user="beginbot", command="add_perms", args=[soundeffect, user]
    ).add_perm()

    msg = f"@{user} now has access to Sound Effect: !{soundeffect}"
    return msg


def drop_soundeffect(invoking_user, args=[]):
    if invoking_user not in STREAM_GODS:
        return
    elif len(args) == 0:
        return drop_random_soundeffect_to_random_user()
    else:
        print("COMING SOON")
        pass
