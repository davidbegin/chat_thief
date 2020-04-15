from pathlib import Path
import re
import subprocess

from tinydb import TinyDB, Query

from chat_thief.irc_msg import IrcMsg
from chat_thief.models import SoundEffect, CommandPermission
from chat_thief.irc import send_twitch_msg
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.audio_player import AudioPlayer


SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"
ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus"]
ADD_SOUND_EFFECT_PATH = Path(SAMPLES_PATH).joinpath("add_sound_effect")

# Do you want the new item and update item sounds
PLAY_UPDATE_EFFECTS = True

soundeffects_db_path = Path(__file__).parent.parent.joinpath("db/soundeffects.json")
DB = TinyDB(soundeffects_db_path)


class SampleSaver:
    def __init__(self, irc_msg: IrcMsg):
        self.user = irc_msg.user
        self.msg = irc_msg.msg
        self.command = irc_msg.command
        self.args = irc_msg.args
        self.soundeffects_table = DB.table("soundeffects")
        self.command_permissions_table = DB.table("command_permissions")

    def save(self):
        youtube_id, name, start_time, end_time = self.args
        # TODO: reject if theres any characters that could wreck our live
        regex = re.compile("^[a-zA-Z0-9_-]*$")
        if not regex.match(name):
            print("WHAT THE HECK ARE YOU DOING")
            return

        print(f"\n{self.user} is trying to add a command: {self.command}\n")

        sample_updated = False
        for sample in self._current_samples():
            print(f"Deleting Previous {sample}")
            if sample.is_file():
                sample.unlink()
                sample_updated = True

        # When should we save
        self._save_command()

        # We need to check if
        # Here is where we save the sample
        subprocess.call(
            [ADD_SOUND_EFFECT_PATH.resolve()] + self.args,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

        if sample_updated:
            new_item = Path(SAMPLES_PATH).joinpath("update.opus")
            send_twitch_msg(f"Updated Sound Available: !{self.args[1]}")
        else:
            new_item = Path(SAMPLES_PATH).joinpath("new_item.wav")
            send_twitch_msg(f"New Sound Available: !{self.args[1]}")

        if PLAY_UPDATE_EFFECTS:
            AudioPlayer.play_sample(new_item)

    def _current_samples(self):
        return [
            Path(SAMPLES_PATH).joinpath(f"{self.args[1]}{suffix}")
            for suffix in ALLOWED_AUDIO_FORMATS
        ]

    def _save_command(self):
        youtube_id, name, start_time, end_time = self.args

        sound = SoundEffect(
            user=self.user,
            youtube_id=youtube_id,
            name=name,
            start_time=start_time,
            end_time=end_time,
        )
        command_permission = CommandPermission(
            user=self.user, command=name, permitted_users=STREAM_LORDS
        )
        print(f"Saving in our DB! {sound.__dict__}")
        self.soundeffects_table.insert(sound.__dict__)
        self.command_permissions_table.insert(command_permission.__dict__)
