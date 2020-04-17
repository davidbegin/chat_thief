from pathlib import Path

import pytest

from chat_thief.user import User
from chat_thief.audio_command import AudioCommand

commands_db_path = Path(__file__).parent.joinpath("db/commands.json")


class TestUser:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if commands_db_path.is_file():
            commands_db_path.unlink()
        yield

    @pytest.fixture
    def user(self):
        def _user(name):
            return User(name=name, commands_db_path=commands_db_path)

        return _user

    @pytest.mark.focus
    def test_commands(self, user):
        subject = user("beginbot")
        assert subject.commands() == []
        audio_command = AudioCommand("flacid", commands_db_path=commands_db_path)
        audio_command.allow_user("beginbot")
        assert audio_command.permitted_users() == ["beginbot"]
        assert subject.commands() == ["flacid"]
