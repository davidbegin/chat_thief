import random

from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.stream_lords import STREAM_LORDS


def random_soundeffect():
    return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]


def random_user():
    looking_for_user = True
    while looking_for_user:
        user = random.sample(WelcomeCommittee.fetch_present_users(), 1)[0]
        if user not in STREAM_LORDS:
            looking_for_user = False
    return user


def drop_soundeffect():
    user = random_user()
    soundeffect = random_soundeffect()
    soundeffect_name = CommandPermissionCenter(
        user="beginbot", command="add_perms", args=[soundeffect, user]
    ).add_permission_for_user(user)

    msg = f"@{user} now has access to Sound Effect: !{soundeffect}"
    return msg
