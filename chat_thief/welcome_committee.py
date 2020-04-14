from pathlib import Path

WELCOME_FILE = Path(__file__).parent.parent.joinpath(".welcome")

# def fetch_present_users_non_streamlords():
#     return set(WelcomeCommittee.fetch_present_users()) - set(STREAM_LORDS)


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

    def welcome(self):
        SOUND_EFFECT_FILES = [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == self.user
        ]

        if SOUND_EFFECT_FILES:
            for effect in SOUND_EFFECT_FILES:
                self.play_soundeffect(effect.resolve())
        else:
            send_twitch_msg(f"You need a theme song! @{self.user}")
            send_twitch_msg(
                "Format: !soundeffect YOUTUBE-ID INSERT_USERNAME 00:03 00:07"
            )

    def welcome_new_users(self):
        if self.user not in WelcomeCommittee.fetch_present_users():
            print(f"\nNew User: {self.user}\n")
            try:
                self.welcome()
            except:
                pass

            with open(WELCOME_FILE, "a") as f:
                f.write(f"{self.user}\n")
