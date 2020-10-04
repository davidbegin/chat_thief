from pathlib import Path

import subprocess
import traceback

from chat_thief.config.log import success
from chat_thief.models.notification import Notification
from chat_thief.models.command import Command

MPLAYER_VOL_NORM = "0.75"


class AudioPlayer:
    @staticmethod
    def play_sample(sound_file, notification=True, user=None):
        sound_name = sound_file.name[: -len(sound_file.suffix)]
        Command(sound_name).decay()

        # success(f"Playing: {sound_name}")

        if notification:
            if user:
                Notification(f"{user}: !{sound_name}", duration=1).save()
            else:
                Notification(f"Playing: !{sound_name}", duration=1).save()

        try:
            pass
            # subprocess.call(
            #     ["mplayer", "-af", f"volnorm=2:{MPLAYER_VOL_NORM}", sound_file],
            #     stderr=subprocess.DEVNULL,
            #     stdout=subprocess.DEVNULL,
            # )
        except:
            traceback.print_exc()
