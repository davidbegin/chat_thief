import subprocess
import traceback

from chat_thief.config.log import success

MPLAYER_VOL_NORM = "0.50"


class AudioPlayer:
    @staticmethod
    def play_sample(sound_file):
        success(f"Playing: {sound_file}")
        try:
            subprocess.call(
                ["mplayer", "-af", f"volnorm=2:{MPLAYER_VOL_NORM}", sound_file],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
        except:
            traceback.print_exc()
