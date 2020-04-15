import pytest

from chat_thief.welcome_committee import WelcomeCommittee


class TestWelcomeCommittee:
    def test_fetch_present_users(self):
        result = WelcomeCommittee.fetch_present_users()
