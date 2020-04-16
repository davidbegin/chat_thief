from pathlib import Path

import pytest

from chat_thief.user import User
from chat_thief.audio_command import AudioCommand


class TestUser:
    db_filepath = Path(__file__).parent.joinpath("db/test.json")

    @classmethod
    def setup_class(cls):
        if cls.db_filepath.is_file():
            cls.db_filepath.unlink()

    @pytest.fixture
    def user(self):
        def _user(name):
            return User(name=name, db_location=self.__class__.db_filepath)

        return _user

    def test_user(self, user):
        subject = user("beginbot")
        assert subject.commands() == []
        audio_command = AudioCommand("flacid", db_location=self.__class__.db_filepath)
        audio_command.allow_user("beginbot")
        assert audio_command.permitted_users() == ["beginbot"]
        assert subject.commands() == ["flacid"]
