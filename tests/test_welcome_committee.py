from pathlib import Path

import pytest

from chat_thief.welcome_committee import WelcomeCommittee

from tests.support.database_setup import DatabaseConfig

welcome_file = Path(__file__).parent.joinpath("db/.welcome")


class TestWelcomeCommittee(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def __setup_welcome__(self):
        if welcome_file.is_file():
            welcome_file.unlink()

    @pytest.fixture
    def welcome_committee(self):
        def _subject():
            return WelcomeCommittee(welcome_file=welcome_file)

        return _subject

    def test_fetch_present_users(self, welcome_committee):
        subject = welcome_committee()
        with open(welcome_file, "w") as wf:
            wf.write("thugga")

        result = subject.present_users()
        assert "thugga" in result

    def test_welcome_new_user(self, welcome_committee):
        subject = welcome_committee()
        result = subject.present_users()
        assert "birdman" not in result
        subject.welcome_new_users("birdman")
        result = subject.present_users()
        assert "birdman" in result
        subject.welcome_new_users("birdman")
        new_result = subject.present_users()
        assert result == new_result
