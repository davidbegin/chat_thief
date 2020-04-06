from typing import Dict, List, Optional
import logging
import os
from pathlib import Path


STREAM_LORDS = [
    "beginbotbot",
    "stupac62",
    "vivax3794",
    "artmattdank",
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
        print("WE ARE TRYING TO PLAY {sound_file}")
        os.system(f"mplayer {sound_file}")

    def build_response(self) -> Optional[str]:
        self.print_msg()

        if self._is_command_msg():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if msg == "!so":
                return self.shoutout()

            # We need to read the file in right here

            WHITELISTED_USERS = Path(__file__).parent.parent.joinpath(
                    ".whitelisted_users").read_text().split()

            print(WHITELISTED_USERS)

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
