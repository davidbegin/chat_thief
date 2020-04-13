from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import re
import subprocess
import traceback

from tinydb import TinyDB, Query

from chat_thief.audio_player import AudioPlayer
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.irc import send_twitch_msg
from chat_thief.models import User, SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.soundeffects_library import SoundeffectsLibrary

ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus"]
SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"

soundeffects_db_path = Path(__file__).parent.parent.joinpath("db/soundeffects.json")
DB = TinyDB(soundeffects_db_path)

# Do you want the new item and update item sounds
PLAY_UPDATE_EFFECTS = True


# These go in permissions
def fetch_present_users_non_streamlords():
    return set(WelcomeCommittee.fetch_present_users()) - set(STREAM_LORDS)


# Separate out adding sound effects
class AudioCommandCenter:
    # TODO: Add Default Logger
    def __init__(self, user: str, msg: str) -> None:
        self.user = user
        self.msg = msg

    def save_command(self, effect_args):
        youtube_id, name, start_time, end_time = effect_args

        # TODO: reject if theres any characters that could wreck our live
        regex = re.compile("^[a-zA-Z0-9_-]*$")
        if not regex.match(name):
            print("WHAT THE HECK ARE YOU DOING")
            return
        else:
            soundeffects_table = DB.table("soundeffects")
            command_permissions_table = DB.table("command_permissions")

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
            soundeffects_table.insert(sound.__dict__)
            command_permissions_table.insert(command_permission.__dict__)

    def save_request(self):
        # Themes don't go to theme folder
        # we don't normalize the type of audio
        soundeffect_requests = Path(__file__).parent.parent.joinpath(".requests")
        previous_requests = soundeffect_requests.read_text().split("\n")
        print(previous_requests)

        request_to_save = self.user + " " + self.msg

        if request_to_save in previous_requests:
            send_twitch_msg(f"Thank you @{self.user} we already have that request")
        else:
            send_twitch_msg(
                f"@{self.user} thank you for your patience in this trying time, beginbot is doing all he can to ensure your safety during this COVID-19 situation. Your request will be processed by a streamlord in due time thanks"
            )
            if self.user != "beginbotbot":
                with open(soundeffect_requests, "a") as f:
                    f.write(request_to_save + "\n")

    def create_new_soundeffect(self):
        print(f"\n\n\n{self.user} is trying to add a command: {self.msg}\n\n\n")
        effect_args = self.msg.split()[1:]

        previous_sfs = [
            Path(SAMPLES_PATH).joinpath(f"{effect_args[1]}{suffix}")
            for suffix in ALLOWED_AUDIO_FORMATS
        ]

        existing_sfs = [sf for sf in previous_sfs if sf.is_file()]

        for sf in existing_sfs:
            print(f"Deleting {sf}")
            sf.unlink()

        add_sound_effect = Path(SAMPLES_PATH).joinpath("add_sound_effect")
        args = [add_sound_effect.resolve()] + effect_args

        try:
            self.save_command(effect_args)
        except Exception as e:
            import traceback

            trace = traceback.format_exc()
            print(f"Error saving command: {e} {trace}")

        subprocess.call(
            args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        )

        if existing_sfs:
            new_item = Path(SAMPLES_PATH).joinpath("update.opus")
            send_twitch_msg(f"Updated Sound Available: !{effect_args[1]}")
        else:
            new_item = Path(SAMPLES_PATH).joinpath("new_item.wav")
            send_twitch_msg(f"New Sound Available: !{effect_args[1]}")

        if PLAY_UPDATE_EFFECTS:
            AudioPlayer.play_sample(new_item)

    def add_command(self):
        if self.user in STREAM_LORDS:
            print("\n\n\nSTREAM LORD!!!!\n\n")
            self.create_new_soundeffect()
        else:
            self.save_request()
        return None

    def audio_command(self, command):
        allowed_users = CommandPermissionCenter().fetch_command_permissions(command)

        if self.user in allowed_users:
            print(f"\n{self.user} is allowed {command}")
        else:
            print(f"\n{self.user} is NOT allowed {command}")

        for sound_file in SoundeffectsLibrary.fetch_soundeffect_samples():
            filename = sound_file.name[: -len(sound_file.suffix)]

            if command == filename:
                if command in SoundeffectsLibrary.fetch_theme_songs():
                    if self.user == command:
                        AudioPlayer.play_sample(sound_file.resolve())
                elif command == "snorlax":
                    if self.user == "artmattdank":
                        AudioPlayer.play_sample(sound_file.resolve())
                else:
                    AudioPlayer.play_sample(sound_file.resolve())

    # this goes somewhere else
    def update_effect_permissions(self):
        if self.user in STREAM_LORDS:
            try:
                # return self.add_permission(self.msg)
                CommandPermissionCenter().add_permission(self.msg)
            except Exception as e:
                trace = traceback.format_exc()
                print(f"Error adding permission: {e} {trace}")
        # elif self.user in
        else:
            print(f"{self.user} cannot add permissions")
