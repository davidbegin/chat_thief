import re

from chat_thief.models.soundeffect_request import SoundeffectRequest


class SoundeffectRequestParser:
    def __init__(self, user, args):
        self.user = user
        self.args = args

        self._set_youtube_id_and_command()
        self._set_start_and_end_time()

    def parse(self):
        # Santize the command
        if self.command.startswith("@") or self.command.startswith("!"):
            self.command = self.command[1:]

        return SoundeffectRequest(
            user=self.user,
            youtube_id=self.youtube_id,
            command=self.command,
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def _set_youtube_id_and_command(self):
        if self._valid_youtube_id(self.args[0]):
            self.youtube_id = self.args[0]
            self.command = self.args[1]
        elif self._valid_youtube_id(self.args[1]):
            self.youtube_id = self.args[1]
            self.command = self.args[0]
        else:
            raise ValueError(f"Did not find a valid Youtube ID in {self.args}")

    def _set_start_and_end_time(self):
        # TODO: handle only a starting time
        # Warn if the time difference is too much
        if len(self.args) == 2:
            self.start_time = "00:00"
            self.end_time = "00:04"
        elif len(self.args) == 3:
            self.command = self.user
            self.start_time = self.args[1]
            self.end_time = self.args[2]
        elif len(self.args) == 4:
            self.start_time = self.args[2]
            self.end_time = self.args[3]
        else:
            raise ValueError("Must pass in a start_time and end_time")

    def _is_valid_url(self, youtube_id):
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

    def _valid_youtube_id(self, youtube_id):
        if len(youtube_id) == 11:
            return True
        elif self._is_valid_url(youtube_id):
            return True
        else:
            return False
