import random
from pathlib import Path
import traceback

from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.chat_logs import ChatLogs
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.command import Command

INVALID_USERS = ["nightbot", ".tim.twitch.tv"] + STREAM_GODS
CONNECTING_MSG = '{"message": "Connecting to #beginbot as beginbotbot"}'


# These should not return theme songs
def random_soundeffect():
    return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]


def random_user(blacklisted_users=[]):
    try:
        looking_for_user = True
        while looking_for_user:
            users = ChatLogs().recent_stream_peasants()
            user = random.sample(users, 1)[0]
            if user not in INVALID_USERS + blacklisted_users:
                looking_for_user = False
        return user
    except:
        traceback.print_exc()
        return None


def drop_effect(user, soundeffect):
    if user not in INVALID_USERS:
        print(f"\n\n\tDROPPING FOR: {user}\n")
        Command(soundeffect).allow_user(user)
        return f"@{user} now has access to Sound Effect: !{soundeffect}"


# WE want to keep looping on random_soundeffect
# until one, is not owned by the user
def drop_random_soundeffect_to_random_user():
    print(f"\n\tUSER: {user}\n")
    user = random_user()
    looking_for_soundeffect = True

    while looking_for_soundeffect:
        soundeffect = random_soundeffect()
        if user not in command(soundeffect).users():
            looking_for_soundeffect = False
    return drop_effect(user, soundeffect)


def _is_int_between(potential_int):
    try:
        return int(potential_int) in range(1, 100)
    except:
        return False


def drop_random_soundeffect_to_user(user):
    # So here is the problem
    # This needs to
    soundeffect = random_soundeffect()
    return drop_effect(user, soundeffect)
