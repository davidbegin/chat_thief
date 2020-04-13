import subprocess
import os

MPLAYER_VOL_NORM = "0.55"

from chat_thief.obs import OBS_COMMANDS


class AudioPlayer:
    @staticmethod
    def play_sample(sound_file):
        print(f"Playing: {sound_file}")
        subprocess.call(
            ["mplayer", "-af", f"volnorm=2:{MPLAYER_VOL_NORM}", sound_file],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    @staticmethod
    def try_soundeffect(user, command, msg):
        if command in OBS_COMMANDS:
            print(f"executing OBS Command: {command}")
            # TODO: update to subprocess
            os.system(f"so {command}")
        elif command in SoundeffectsLibrary.fetch_soundeffect_names():
            AudioCommandCenter(user=user, command=command, msg=msg).audio_command(
                command
            )
            # self.audio_command_center.audio_command(command)
