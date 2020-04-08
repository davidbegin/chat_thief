from typing import Dict, List, Optional
import logging
import os
from pathlib import Path
import subprocess

from chat_thief.irc import send_twitch_msg

# TODO: Whitelist command
# Blacklist Command

# We need stream lords
STREAM_LORDS = [
    "beginbotbot",
    "stupac62",
    "vivax3794",
    "artmattdank",
    "baldclap",
    "tramstarzz",
]

OBS_COMMANDS = [
    "wyp",
    "idk",
    "jdi",
    "brb",
]

ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus"]

SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"

THEME_SONGS_PATH = "/home/begin/stream/Stream/Samples/theme_songs"

WELCOME_FILE = Path(__file__).parent.parent.joinpath(".welcome")

# !whitelist


def fetch_whitelisted_users():
    return (
        Path(__file__).parent.parent.joinpath(".whitelisted_users").read_text().split()
    )


def fetch_theme_songs():
    return [
        theme.name[: -len(theme.suffix)] for theme in Path(THEME_SONGS_PATH).glob("*")
    ]


def fetch_soundeffect_samples():
    return {
        p.resolve()
        for p in Path(SAMPLES_PATH).glob("**/*")
        if p.suffix in ALLOWED_AUDIO_FORMATS
    }


def fetch_soundeffect_names():
    return {
        sound_file.name[: -len(sound_file.suffix)]
        for sound_file in fetch_soundeffect_samples()
    }


def fetch_present_users():
    if WELCOME_FILE.is_file():
        return WELCOME_FILE.read_text().split()
    else:
        WELCOME_FILE.touch()
        return []


class CommandParser:
    # TODO: Add Default Logger
    def __init__(self, irc_msg: List[str], logger: logging.Logger) -> None:
        self._irc_msg = irc_msg
        self._logger = logger
        user_info, _, _, *raw_msg = self._irc_msg
        self.user = user_info.split("!")[0][1:]
        self.msg = self._msg_sanitizer(raw_msg)

    def print_msg(self) -> None:
        self._logger.info(f"{self.user}: {self.msg}")

    def play_sample(self, sound_file):
        print(f"Playing: {sound_file}")
        subprocess.call(
            ["mplayer", sound_file],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    def welcome(self):
        print(f"Welcome: {self.user}")
        SOUND_EFFECT_FILES = [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == self.user
        ]

        for effect in SOUND_EFFECT_FILES:
            os.system(f"mplayer {effect.resolve()}")

    def add_command(self):
        if self.user in STREAM_LORDS:
            print("\n\n\nSTREAM LORD!!!!\n\n")
            print(f"\n\n\n{self.user} is trying to add a command: {self.msg}\n\n\n")
            effect_args = self.msg.split()[1:]
            os.system(
                f"/home/begin/stream/Stream/Samples/add_sound_effect {' '.join(effect_args) }"
            )
        return None

    def welcome_new_users(self):
        if self.user not in fetch_present_users():
            print(f"\nNew User: {self.user}\n")
            try:
                self.welcome()
            except:
                send_twitch_msg(f"You need a theme song! @{self.user}")
                send_twitch_msg(
                    "Format: soundeffect YOUTUBE-ID INSERT_USERNAME 00:03 00:07"
                )

            with open(WELCOME_FILE, "a") as f:
                f.write(f"{self.user}\n")

    def audio_command(self, command):
        for sound_file in fetch_soundeffect_samples():
            filename = sound_file.name[: -len(sound_file.suffix)]
            if command == filename:
                if command in fetch_theme_songs():
                    if self.user == command:
                        self.play_sample(sound_file.resolve())
                elif command == "snorlax":
                    if self.user == "artmattdank":
                        self.play_sample(sound_file.resolve())
                else:
                    self.play_sample(sound_file.resolve())

    def build_response(self) -> Optional[str]:
        self.print_msg()
        self.welcome_new_users()

        if self._is_command_msg():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if msg == "!so":
                return self.shoutout()

            if msg == "!whitelist":
                print("WHITELIST")
                return " ".join(fetch_whitelisted_users())

            if msg == "!soundeffect":
                return self.add_command()

            if self.user in fetch_whitelisted_users():
                if command in OBS_COMMANDS:
                    print(f"executing OBS Command: {msg}")
                    os.system(f"so {command}")
                elif command in fetch_soundeffect_names():
                    self.audio_command(command)

        return None

    def _msg_sanitizer(self, msg: List[str]) -> str:
        first, *rest = msg
        return f"{first[1:]} {' '.join(rest)}"

    def _is_command_msg(self) -> bool:
        return self.msg[0] == "!" and self.msg[1] != "!"

    def shoutout(self) -> str:
        msg_segs = self.msg.split()

        if len(msg_segs) > 1 and msg_segs[1].startswith("@"):
            return f"Shoutout twitch.tv/{msg_segs[1][1:]}"
        else:
            return f"Shoutout twitch.tv/{msg_segs[1]}"
