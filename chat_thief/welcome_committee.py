from pathlib import Path
import traceback

from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SAMPLES_PATH, ALLOWED_AUDIO_FORMATS
from chat_thief.audio_player import AudioPlayer
from chat_thief.prize_dropper import drop_random_soundeffect_to_user
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest


from chat_thief.welcome_file import WelcomeFile, WELCOME_FILE


class WelcomeCommittee:
    def __init__(self, user):
        self.user = user

    def welcome_new_users(self):
        # drop_random_soundeffect_to_user(self.user)

        if self.user not in WelcomeFile.present_users():
            print(f"\nNew User: {self.user}\n")
            try:
                self.welcome()
            except:
                traceback.print_exc()

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
            effect = sound_effect_files[0]
            PlaySoundeffectRequest(user=self.user, command=self.user).save()
        else:
            send_twitch_msg(f"You need a theme song! @{self.user}")
            send_twitch_msg(
                "Format: !soundeffect YOUTUBE-ID INSERT_USERNAME 00:03 00:07"
            )
