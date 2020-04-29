from pathlib import Path


import pytest

from chat_thief.models.user import User
from chat_thief.audio_command import AudioCommand

commands_db_path = Path(__file__).parent.parent.joinpath("db/commands.json")
users_db_path = Path(__file__).parent.parent.joinpath("db/users.json")


class TestUser:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if commands_db_path.is_file():
            commands_db_path.unlink()
        if users_db_path.is_file():
            users_db_path.unlink()
        yield

    @pytest.fixture
    def user(self):
        def _user(name):
            return User(
                name=name,
                users_db_path=users_db_path,
                commands_db_path=commands_db_path,
            )

        return _user

    def test_commands(self, user):
        subject = user("artmattdank")
        assert subject.commands() == []
        audio_command = AudioCommand("flacid", commands_db_path=commands_db_path)
        audio_command.allow_user("artmattdank")
        assert audio_command.permitted_users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]

    def test_add_street_cred(self, user):
        subject = user("artmattdank")
        assert subject.street_cred() == 0
        subject.add_street_cred()
        assert subject.street_cred() == 1

    def test_remove_all_commands(self, user):
        subject = user("artmattdank")
        assert subject.commands() == []
        audio_command = AudioCommand("flacid", commands_db_path=commands_db_path)
        audio_command.allow_user("artmattdank")
        assert audio_command.permitted_users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]
        subject.remove_all_commands()
        assert subject.commands() == []
        assert audio_command.permitted_users() == []
