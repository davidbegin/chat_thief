from typing import Dict, List, Optional
import logging
import os
from pathlib import Path


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

# We also need separate sound Affects

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
        print(f"WE ARE TRYING TO PLAY {sound_file}")
        os.system(f"mplayer {sound_file}")

    def welcome(self):
        print(f"WE ARE TRYING TO PLAY {self.user}")
        # Need need to add the user name to the .welcome)
        # We need to find the write sample name
        SOUND_EFFECT_FILES = [
            p for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[:-len(p.suffix)] == self.user
        ]

        for effect in SOUND_EFFECT_FILES:
            os.system(f"mplayer {effect.resolve()}")

        # path = Path(__file__).parent.parent.parent.parent.joinpath(f"stream/Stream/Samples/{self.user}.m4a")
        # This must add to the welcome file


    def add_command(self):
        if self.user in STREAM_LORDS:
            print("\n\n\nSTREAM LORD!!!!\n\n")
            print(f"\n\n\n{self.user} is trying to add a command: {self.msg}\n\n\n")

            command = self.msg[1:].split()[0]
            effect_args = self.msg.split()[1:]

            # ['Xs6_vecSv2Y', 'correct', '05:08', '05:11']
            os.system(
                f"/home/begin/stream/Stream/Samples/add_sound_effect {' '.join(effect_args) }"
            )



    def build_response(self) -> Optional[str]:
        self.print_msg()

        try:
            welcome_file = Path(__file__).parent.parent.joinpath(".welcome")
            present_viewers = welcome_file.read_text().split()
        except:
            present_viewers = []

        if self.user not in present_viewers:
            print(f"\n\nNew User: {self.user}\n\n")
            try:
                self.welcome()
            except:
                print("WE need a soundeffect")

            with open(welcome_file, "a") as f:
                f.write(f"{self.user}\n")

        if self._is_command_msg():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if msg == "!so":
                return self.shoutout()

            if command == "soundeffect":
                return self.add_command()

            # We need to read the file in right here

            WHITELISTED_USERS = Path(__file__).parent.parent.joinpath(
                    ".whitelisted_users").read_text().split()

            # print(WHITELISTED_USERS)

            if self.user in WHITELISTED_USERS:
                SOUND_AFFECT_FILES = {
                    p.resolve() for p in Path(SAMPLES_PATH).glob("**/*")
                    if p.suffix in ALLOWED_AUDIO_FORMATS
                }
                SOUND_AFFECTS = {
                    sound_file.name[:-len(sound_file.suffix)] for sound_file in SOUND_AFFECT_FILES
                }

                if command in OBS_COMMANDS:
                    print(f"executing OBS Command: {msg}")
                    os.system(f"so {command}")
                elif command in SOUND_AFFECTS:
                    print(f"executing Sound Command: {msg}")

                    for sound_file in SOUND_AFFECT_FILES:
                        filename = sound_file.name[:-len(sound_file.suffix)]

                        if command == filename:
                            theme_songs = Path(__file__).parent.parent.joinpath(".theme_songs").read_text().split()

                            if command in theme_songs:
                                if self.user == command:
                                    self.play_sample(sound_file.resolve())
                            elif command == "snorlax":
                                if self.user == "artmattdank":
                                    self.play_sample(sound_file.resolve())
                            else:
                                self.play_sample(sound_file.resolve())
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
