from typing import Dict, List, Optional
import logging
import os
from pathlib import Path
from dataclasses import dataclass
import subprocess

from tinydb import TinyDB, Query

from chat_thief.obs import OBS_COMMANDS
from chat_thief.irc import send_twitch_msg
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.audio_command_center import (
    AudioCommandCenter,
    fetch_soundeffect_names,
    remove_completed_requests,
)

# We might wat to move this


def fetch_whitelisted_users():
    return (
        Path(__file__).parent.parent.joinpath(".whitelisted_users").read_text().split()
    )


# Separate out adding sound effects
class CommandParser:
    # TODO: Add Default Logger
    def __init__(self, irc_msg: List[str], logger: logging.Logger) -> None:
        self._irc_msg = irc_msg
        self._logger = logger
        user_info, _, _, *raw_msg = self._irc_msg
        self.user = user_info.split("!")[0][1:]
        self.msg = self._msg_sanitizer(raw_msg)
        self.audio_command_center = AudioCommandCenter(user=self.user, msg=self.msg)

    def print_msg(self) -> None:
        self._logger.info(f"{self.user}: {self.msg}")

    def handle_them_requests(self):
        try:
            remove_completed_requests()
        except Exception as e:
            print(f"Error Removing Message: {e}")

        soundeffect_requests = Path(__file__).parent.parent.joinpath(".requests")
        previous_requests = soundeffect_requests.read_text().split("\n")

        if previous_requests:
            for sound_request in previous_requests:
                if sound_request:
                    send_twitch_msg("Request: " + sound_request)
        else:
            send_twitch_msg("No Requests! Great Job STREAM_LORDS")

    def try_soundeffect(self, command, msg):
        if command in OBS_COMMANDS:
            print(f"executing OBS Command: {msg}")
            os.system(f"so {command}")
        elif command in fetch_soundeffect_names():
            self.audio_command_center.audio_command(command)

    def build_response(self) -> Optional[str]:
        self.print_msg()
        self.audio_command_center.welcome_new_users()

        if self._is_command_msg():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if msg == "!so":
                return self.shoutout()

            if msg == "!whitelist":
                return " ".join(fetch_whitelisted_users())

            if msg == "!streamlords":
                return " ".join(STREAM_LORDS)

            if msg == "!requests":
                return self.handle_them_requests()

            if msg == "!soundeffect":
                return self.audio_command_center.add_command()

            if self.user in fetch_whitelisted_users():
                self.try_soundeffect(command, msg)

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
