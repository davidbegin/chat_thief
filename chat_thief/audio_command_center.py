from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import re
import subprocess
import traceback

from chat_thief.audio_player import AudioPlayer
from chat_thief.irc import send_twitch_msg
from chat_thief.models import User, SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.irc_msg import IrcMsg
from chat_thief.request_saver import RequestSaver
from chat_thief.sample_saver import SampleSaver


class AudioCommandCenter:
    """
    In charge of saving new audio samples, and requests
    """

    def __init__(self, irc_msg: IrcMsg) -> None:
        self.irc_msg = irc_msg
        self.user = irc_msg.user
        self.msg = irc_msg.msg
        self.command = irc_msg.command
        self.args = irc_msg.args

    def add_command(self):
        if self.user in STREAM_LORDS:
            SampleSaver(self.irc_msg).save()
        else:
            print("Not a Streamlord, so we are attempting to save you sample")
            RequestSaver(self.user, self.msg).save()

    def play_audio_command(self):
        sound_files = [
            sound_file
            for sound_file in SoundeffectsLibrary.fetch_soundeffect_samples()
            if sound_file.name[: -len(sound_file.suffix)] == self.command
        ]
        for sound_file in sound_files:
            AudioPlayer.play_sample(sound_file.resolve())
