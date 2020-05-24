from pathlib import Path

import subprocess
import traceback

from chat_thief.config.log import success
from chat_thief.models.notification import Notification

MPLAYER_VOL_NORM = "0.50"


class AudioPlayer:
    @staticmethod
    def play_sample(sound_file):
        sound_name = sound_file.name[: -len(sound_file.suffix)]
        success(f"Playing: {sound_name}")
        Notification(f"Playing: {sound_name}").save()

        try:
            subprocess.call(
                ["mplayer", "-af", f"volnorm=2:{MPLAYER_VOL_NORM}", sound_file],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
        except:
            traceback.print_exc()
