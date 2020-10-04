from pathlib import Path
import re
import os
import subprocess

from chat_thief.irc_msg import IrcMsg
from chat_thief.irc import send_twitch_msg
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.prize_dropper import random_user
from chat_thief.models.command import Command
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest


SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"
ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus", ".webm"]
ADD_SOUND_EFFECT_PATH = Path(SAMPLES_PATH).joinpath("add_sound_effect")


class SampleSaver:
    def __init__(self, user, youtube_id, command, start_time, end_time):
        self.user = user
        self.youtube_id = youtube_id
        self.start_time = start_time
        self.end_time = end_time
        self.name = self._sanitize_command(command)

    def save(self, requester=None):
        print(f"\n{self.user} is trying to add a command: {self.name}\n")
        self._validate_sample_name()

        # Testing Logic in production code???!  #😞
        if "TEST_MODE" not in os.environ:
            sample_updated = self._delete_old_sample()
            self._save_with_youtube_dl()
            self._notify(sample_updated)

        command = Command(name=self.name)

        # We need to make sure to save the requester
        if command.exists():
            command.allow_user(random_user())
        else:
            command.save()

        if requester:
            command.allow_user(requester)

    def _notify(self, sample_updated):
        if sample_updated:
            send_twitch_msg(f"Updated Sound Available: !{self.name}")
        else:
            send_twitch_msg(f"New Sound Available: !{self.name}")

    def _delete_old_sample(self):
        samples = Path(SAMPLES_PATH).glob(f"**/{self.name}.*")

        sample_updated = False
        for sample in samples:
            print(f"Deleting Previous {sample}")
            if sample.is_file():
                sample.unlink()
                sample_updated = True
        return sample_updated

    def _sanitize_command(self, command):
        command = command.lower()

        if command.startswith("@") or command.startswith("!"):
            command = command[1:]
        return command

    # Maybe: This belongs in the soundeffects library

    # We are iterating through a list of types of audio formats
    # and doing exact matches
    # we should instead just match the name
    def _current_samples(self):
        return [
            Path(SAMPLES_PATH).joinpath(f"{self.name}{suffix}")
            for suffix in ALLOWED_AUDIO_FORMATS
        ]

    # We need to be doing this in python instead
    def _save_with_youtube_dl(self):
        subprocess.call(
            [ADD_SOUND_EFFECT_PATH.resolve()] + self._add_soundeffect_args()
            # stderr=subprocess.DEVNULL,
            # stdout=subprocess.DEVNULL,
        )

    def _add_soundeffect_args(self):
        args = [self.youtube_id, self.name, self.start_time, self.end_time]
        if self.name in WelcomeCommittee().present_users():
            args = args + ["theme"]
        return args

    def _validate_sample_name(self):
        regex = re.compile("^[a-zA-Z0-9_-]*$")
        if not regex.match(self.name):
            raise ValueError(f"THAT IS NOT A VALID NAME FOR A COMMAND: {self.name}")
