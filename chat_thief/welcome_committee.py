from pathlib import Path
import traceback

from chat_thief.soundeffects_library import SAMPLES_PATH, ALLOWED_AUDIO_FORMATS
from chat_thief.audio_player import AudioPlayer

WELCOME_FILE = Path(__file__).parent.parent.joinpath(".welcome")


class WelcomeCommittee:
    @staticmethod
    def fetch_present_users():
        if WELCOME_FILE.is_file():
            return WELCOME_FILE.read_text().split()
        else:
            WELCOME_FILE.touch()
            return []

    def __init__(self, user):
        self.user = user

    def welcome_new_users(self):
        if self.user not in WelcomeCommittee.fetch_present_users():
            print(f"\nNew User: {self.user}\n")
            try:
                self.welcome()
            except Exception as e:
                print(e, traceback.format_exc())

            with open(WELCOME_FILE, "a") as f:
                f.write(f"{self.user}\n")

    def welcome(self):
        sound_effect_files = [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == self.user
        ]

        if sound_effect_files:
            for effect in sound_effect_files:
                AudioPlayer.play_sample(effect.resolve())
        else:
            send_twitch_msg(f"You need a theme song! @{self.user}")
            send_twitch_msg(
                "Format: !soundeffect YOUTUBE-ID INSERT_USERNAME 00:03 00:07"
            )
