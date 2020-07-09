import re
from typing import List, Dict, Any, Optional, NoReturn, Union

from chat_thief.models.soundeffect_request import SoundeffectRequest


class SoundeffectRequestParser:
    def __init__(self, user: str, args: List[str] = []):
        self.user = user
        self.args = args
        self.start_time = "00:00"
        self.end_time = "00:04"
        self.youtube_id = None

        self._set_youtube_id_and_command()
        self._set_start_and_end_time()

    def parse(self) -> Optional[SoundeffectRequest]:
        # Santize the command
        if self.command.startswith("@") or self.command.startswith("!"):
            self.command = self.command[1:]

        if self.youtube_id is None:
            raise ValueError("Could not Find Valid URL")

        return SoundeffectRequest(
            user=self.user,
            youtube_id=self.youtube_id,
            command=self.command,
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def _set_youtube_id_and_command(self) -> None:
        for arg in self.args:
            if self._valid_youtube_id(arg):
                self.youtube_id = arg

        if len(self.args) > 1:
            new_args = self.args.copy()
            if self.youtube_id:
                new_args.remove(self.youtube_id)
            self.command = new_args[0]
        else:
            self.command = self.user

        if self.youtube_id is None and self.command is None:
            raise ValueError(f"Did not find a valid Youtube ID in {self.args}")

    # TODO: handle only a starting time
    # Warn if the time difference is too much
    def _set_start_and_end_time(self) -> None:
        if len(self.args) == 3:
            self.command = self.user
            self.start_time = self.args[1]
            self.end_time = self.args[2]
        elif len(self.args) == 4:
            self.start_time = self.args[2]
            self.end_time = self.args[3]

    def _is_valid_url(self, youtube_id: str) -> bool:
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        return re.match(regex, youtube_id) is not None

    def _valid_youtube_id(self, youtube_id: str) -> bool:
        return self._is_valid_url(youtube_id)
