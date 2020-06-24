import random
from pathlib import Path
import traceback
from collections import defaultdict

from chat_thief.models.command import Command
from chat_thief.models.the_fed import TheFed
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.chat_logs import ChatLogs

INVALID_USERS = ["nightbot", ".tim.twitch.tv"] + STREAM_GODS
CONNECTING_MSG = '{"message": "Connecting to #beginbot as beginbotbot"}'


def random_soundeffect():
    return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]


def drop_effect(user, soundeffect):
    if user not in INVALID_USERS:
        print(f"\n\n\tDROPPING FOR: {user}\n")
        command = Command(soundeffect)
        TheFed.pay(command.cost())
        command.allow_user(user)
        return (user, soundeffect)


class BeginFund:
    def __init__(self, target_user=None, target_command=None, amount=None):
        self._target_user = target_user
        self._target_command = target_command
        self._amount = amount

    def dropeffect(self):
        if TheFed.reserve() == 0:
            return "The Fed is Broke"

        return self.drop()

    def drop(self):
        if self._amount:
            results = []
            for i in range(0, self._amount):
                results.append(self._drop())

            grouped_results = defaultdict(list)

            for user, command in results:
                grouped_results[command].append(f"@{user}")

            return " | ".join(
                [
                    f"{', '.join(users)} now has access to !{command}"
                    for command, users in grouped_results.items()
                ]
            )

        user, command = self._drop()
        return f"@{user} now has access to !{command}"

    def _drop(self):
        if self._target_user and self._target_command:
            return drop_effect(self._target_user, self._target_command)
        elif self._target_user:
            return self.drop_random_soundeffect_to_user(self._target_user)
        elif self._target_command:
            return self.drop_soundeffect_for_random_user(self._target_command)
        else:
            return self.drop_random_soundeffect_to_random_user()

    def drop_soundeffect_for_random_user(self, soundeffect):
        user = self.random_user()
        return drop_effect(user, soundeffect)

    def drop_random_soundeffect_to_user(self, user):
        soundeffect = random_soundeffect()
        return drop_effect(user, soundeffect)

    def drop_random_soundeffect_to_random_user(self):
        user = self.random_user()
        soundeffect = random_soundeffect()
        return drop_effect(user, soundeffect)

    def random_user(self, blacklisted_users=[]):
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
