from pathlib import Path

WELCOME_FILE = Path(__file__).parent.parent.joinpath(".welcome")


class WelcomeCommittee:
    @staticmethod
    def fetch_present_users():
        if WELCOME_FILE.is_file():
            return WELCOME_FILE.read_text().split()
        else:
            WELCOME_FILE.touch()
            return []
