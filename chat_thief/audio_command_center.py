from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import subprocess

from tinydb import TinyDB, Query

from chat_thief.irc import send_twitch_msg
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.command_permissions import CommandPermissionCenter

from chat_thief.models import User, SoundEffect, CommandPermission

OBS_COMMANDS = [
    "wyp",
    "idk",
    "jdi",
    "brb",
]

ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus"]
SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"
THEME_SONGS_PATH = "/home/begin/stream/Stream/Samples/theme_songs"
WELCOME_FILE = Path(__file__).parent.parent.joinpath(".welcome")
MPLAYER_VOL_NORM = "0.55"

soundeffects_db_path = Path(__file__).parent.parent.joinpath("db/soundeffects.json")
DB = TinyDB(soundeffects_db_path)

# Do you want the new item and update item sounds
PLAY_UPDATE_EFFECTS = True


def fetch_theme_songs():
    return [
        theme.name[: -len(theme.suffix)] for theme in Path(THEME_SONGS_PATH).glob("*")
    ]


def fetch_soundeffect_samples():
    return {
        p.resolve()
        for p in Path(SAMPLES_PATH).glob("**/*")
        if p.suffix in ALLOWED_AUDIO_FORMATS
    }


def fetch_soundeffect_names():
    return [
        sound_file.name[: -len(sound_file.suffix)]
        for sound_file in fetch_soundeffect_samples()
    ]


def fetch_present_users():
    if WELCOME_FILE.is_file():
        return WELCOME_FILE.read_text().split()
    else:
        WELCOME_FILE.touch()
        return []


def remove_completed_requests():
    soundeffect_names = fetch_soundeffect_names()
    print(f"\n\n{soundeffect_names}\n\n")
    soundeffect_requests = Path(__file__).parent.parent.joinpath(".requests")

    unfulfilled_requests = [
        request
        for request in soundeffect_requests.read_text().strip().split("\n")
        if request.split()[3] not in soundeffect_names
    ]

    print(f"\n\nUnfulfilled Request: {unfulfilled_requests}\n\n")
    with open(soundeffect_requests, "w") as f:
        if unfulfilled_requests:
            f.write("\n".join(unfulfilled_requests) + "\n")
        else:
            f.write("")


# Separate out adding sound effects
class AudioCommandCenter:
    # TODO: Add Default Logger
    def __init__(self, user: str, msg: str) -> None:
        self.user = user
        self.msg = msg

    def play_sample(self, sound_file):
        print(f"Playing: {sound_file}")
        subprocess.call(
            ["mplayer", "-af", f"volnorm=2:{MPLAYER_VOL_NORM}", sound_file],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    def welcome(self):
        SOUND_EFFECT_FILES = [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == self.user
        ]

        for effect in SOUND_EFFECT_FILES:
            self.play_soundeffect(effect.resolve())

    def play_soundeffect(self, effect_path):
        subprocess.call(
            ["mplayer", "-af", "volnorm=2:0.5", effect_path],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    def save_command(self, effect_args):
        youtube_id, name, start_time, end_time = effect_args

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
            self.play_soundeffect(new_item)

    def add_command(self):
        if self.user in STREAM_LORDS:
            print("\n\n\nSTREAM LORD!!!!\n\n")
            self.create_new_soundeffect()
        else:
            self.save_request()
        return None

    def welcome_new_users(self):
        if self.user not in fetch_present_users():
            print(f"\nNew User: {self.user}\n")
            try:
                self.welcome()
            except:
                send_twitch_msg(f"You need a theme song! @{self.user}")
                send_twitch_msg(
                    "Format: soundeffect YOUTUBE-ID INSERT_USERNAME 00:03 00:07"
                )

            with open(WELCOME_FILE, "a") as f:
                f.write(f"{self.user}\n")

    def audio_command(self, command):
        allowed_users = CommandPermissionCenter().fetch_command_permissions(command)

        if self.user in allowed_users:
            print(f"\n{self.user} is allowed {command}")
        else:
            print(f"\n{self.user} is NOT allowed {command}")

        for sound_file in fetch_soundeffect_samples():
            filename = sound_file.name[: -len(sound_file.suffix)]

            # We need to check if the user is allowed to use this command

            if command == filename:
                if command in fetch_theme_songs():
                    if self.user == command:
                        self.play_sample(sound_file.resolve())
                elif command == "snorlax":
                    if self.user == "artmattdank":
                        self.play_sample(sound_file.resolve())
                else:
                    self.play_sample(sound_file.resolve())
