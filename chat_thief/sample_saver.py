from pathlib import Path
import re
import subprocess

from tinydb import TinyDB, Query

from chat_thief.irc_msg import IrcMsg
from chat_thief.models.soundeffect import SoundEffect
from chat_thief.models.command_permission import CommandPermission
from chat_thief.irc import send_twitch_msg
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.audio_player import AudioPlayer
from chat_thief.welcome_file import WelcomeFile
from chat_thief.prize_dropper import random_user
from chat_thief.audio_command import AudioCommand
from chat_thief.new_models.play_soundeffect_request import PlaySoundeffectRequest


SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"
ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus"]
ADD_SOUND_EFFECT_PATH = Path(SAMPLES_PATH).joinpath("add_sound_effect")

soundeffects_db_path = Path(__file__).parent.parent.joinpath("db/soundeffects.json")
DB = TinyDB(soundeffects_db_path)

from chat_thief.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH


class SampleSaver:
    def __init__(self, user, youtube_id, command, start_time, end_time):
        self.user = user

        self.soundeffects_table = DB.table("soundeffects")
        self.command_permissions_table = DB.table("command_permissions")

        self.name = command.lower()
        self.youtube_id = youtube_id
        self.start_time = start_time
        self.end_time = end_time

    def _add_soundeffect_args(self):
        # Who calls SampleSaver?
        # Right here, are these args in the right order?
        args = [self.youtube_id, self.name, self.start_time, self.end_time]
        if self.name in WelcomeFile.present_users():
            args = args + ["theme"]
        return args

    def save(self, requester=None):
        regex = re.compile("^[a-zA-Z0-9_-]*$")
        if not regex.match(self.name):
            # Autotime out?
            print(f"THAT IS NOT A VALID NAME FOR A COMMAND: {self.name}")
            return

        print(f"\n{self.user} is trying to add a command: {self.name}\n")

        sample_updated = False
        for sample in self._current_samples():
            print(f"Deleting Previous {sample}")
            if sample.is_file():
                sample.unlink()
                sample_updated = True

        # When should we save
        self._save_command()

        # TODO: We need some process around not actually saving during tests
        # We need to be doing this in python instead

        # more directly
        self._save_with_youtube_dl()

        if sample_updated:
            PlaySoundeffectRequest(user="beginbot", command="update").save()
            send_twitch_msg(f"Updated Sound Available: !{self.name}")
        else:
            PlaySoundeffectRequest(user="beginbot", command="new_item").save()
            send_twitch_msg(f"New Sound Available: !{self.name}")

        if requester:
            AudioCommand(self.name).allow_user(requester)

    def _current_samples(self):
        return [
            Path(SAMPLES_PATH).joinpath(f"{self.name}{suffix}")
            for suffix in ALLOWED_AUDIO_FORMATS
        ]

    def _save_command(self):
        sound = SoundEffect(
            user=self.user,
            youtube_id=self.youtube_id,
            name=self.name,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        command_permission = CommandPermission(
            user=self.user, command=self.name, permitted_users=[random_user()]
        )
        # We need the name of the audio commmand
        # AudioCommand(name).allow_user(requester)
        print(f"Saving in our DB! {sound.__dict__}")
        self.soundeffects_table.insert(sound.__dict__)
        self.command_permissions_table.insert(command_permission.__dict__)

    def _save_with_youtube_dl(self):
        """
        if [[ -z "$5" ]]
        then
          SAMPLES_PATH="/home/begin/stream/Stream/Samples"
        else
          echo "ITS A THEME!"
          SAMPLES_PATH="/home/begin/stream/Stream/Samples/theme_songs"
        fi

        if [[ -z "$3" && -z "$4" ]]
        then
          youtube-dl -x "$1" -o "$2.%(ext)s"
        else
          echo "Cutting from $3 to $4"
          youtube-dl -x --postprocessor-args "-ss $3 -to $4" $1 -o "$SAMPLES_PATH/$2.%(ext)s"
        fi
        """
        subprocess.call(
            [ADD_SOUND_EFFECT_PATH.resolve()] + self._add_soundeffect_args(),
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        pass
