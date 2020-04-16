import random
from pathlib import Path

from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.audio_command import AudioCommand


def random_soundeffect():
    return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]


def random_user():
    looking_for_user = True
    while looking_for_user:
        user = random.sample(WelcomeCommittee.fetch_present_users(), 1)[0]
        if user not in STREAM_LORDS and user != "nightbot":
            looking_for_user = False
    return user


def drop_effect(user, soundeffect):
    AudioCommand(soundeffect).allow_user(user)
    msg = f"@{user} now has access to Sound Effect: !{soundeffect}"
    return msg


def drop_random_soundeffect_to_random_user():
    user = random_user()
    soundeffect = random_soundeffect()
    return drop_effect(user, soundeffect)


INVALID_USERS = ["nightbot",] + STREAM_LORDS

CONNECTING_MSG = '{"message": "Connecting to #beginbot as beginbotbot"}'


def dropreward():
    with Path(__file__).parent.parent.joinpath("logs/chat.log") as log:
        chat_lines = [
            line
            for line in log.read_text().split("\n")
            if line
            and line.split(":")[0] not in INVALID_USERS
            and line != CONNECTING_MSG
        ]
    user = chat_lines[-1].split(":")[0]
    soundeffect = random_soundeffect()
    return drop_effect(user, soundeffect)


# This needs a stronger interface
def drop_soundeffect(invoking_user, args=[]):
    if len(args) == 0:
        return drop_random_soundeffect_to_random_user()
    else:
        if args[0] in WelcomeCommittee.fetch_present_users():
            user = args[0]
            soundeffect = random_soundeffect()
            return drop_effect(user, soundeffect)
        elif args[0] in SoundeffectsLibrary.fetch_soundeffect_names():
            user = random_user()
            soundeffect = args[0]
            return drop_effect(user, soundeffect)
