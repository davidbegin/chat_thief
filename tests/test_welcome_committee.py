import pytest

from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.welcome_file import WelcomeFile


class TestWelcomeCommittee:
    def test_fetch_present_users(self):
        result = WelcomeFile.present_users()
