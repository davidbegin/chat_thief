from chat_thief.models.soundeffect_request import SoundeffectRequest


class SoundeffectRequestParser:
    def __init__(self, user, args):
        self.user = user
        self.args = args

        self._set_youtube_id_and_command()
        self._set_start_and_end_time()

    def parse(self):
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
        elif len(self.args) == 4:
            self.start_time = self.args[2]
            self.end_time = self.args[3]
        else:
            raise ValueError("Must pass in a start_time and end_time")

    def _valid_youtube_id(self, youtube_id):
        return len(youtube_id) == 11
