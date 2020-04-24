from pathlib import Path
import traceback

from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SAMPLES_PATH, ALLOWED_AUDIO_FORMATS
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest


DEFAULT_WELCOME_FILE = Path(__file__).parent.parent.joinpath(".welcome")


class WelcomeCommittee:
    def __init__(self, welcome_file=DEFAULT_WELCOME_FILE):
        self.welcome_file = welcome_file

    def present_users(self):
        if self.welcome_file.is_file():
            return self.welcome_file.read_text().split()
        else:
            self.welcome_file.touch()
            return []

    def welcome_new_users(self, user):
        if user not in self.present_users():
            print(f"\nNew User: {user}\n")
            try:
                self.welcome()
            except:
                traceback.print_exc()

            with open(self.welcome_file, "a") as f:
                f.write(f"{user}\n")

    def welcome(self, user):
        sound_effect_files = [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == user
        ]

        if sound_effect_files:
            effect = sound_effect_files[0]
            PlaySoundeffectRequest(user=user, command=user).save()
        else:
            send_twitch_msg(
                f"You need a Theme song (max 5 secs): !soundeffect YOUTUBE-ID @{user} 00:03 00:07"
            )
