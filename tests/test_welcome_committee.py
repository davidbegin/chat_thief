from pathlib import Path

import pytest

from chat_thief.welcome_committee import WelcomeCommittee


# How would I like to interact with the Committee


class TestWelcomeCommittee:
    @pytest.mark.focus
    def test_fetch_present_users(self):
        welcome_file = Path(__file__).parent.parent.joinpath("db/.welcome")
        result = WelcomeCommittee(welcome_file=welcome_file).present_users()
        # breakpoint()
        print(result)
