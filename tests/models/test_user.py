from pathlib import Path


import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote

commands_db_path = Path(__file__).parent.parent.joinpath("db/commands.json")
users_db_path = Path(__file__).parent.parent.joinpath("db/users.json")
sfx_votes_db = Path(__file__).parent.parent.joinpath("db/sfx_votes.json")

Command.database_folder = "tests/"
SFXVote.database_folder = "tests/"


class TestUser:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if commands_db_path.is_file():
            commands_db_path.unlink()
        if users_db_path.is_file():
            users_db_path.unlink()
        if sfx_votes_db.is_file():
            sfx_votes_db.unlink()
        yield

    @pytest.fixture
    def user(self):
        def _user(name):
            return User(name=name,)

        return _user

    def test_commands(self, user):
        subject = user("artmattdank")
        assert subject.commands() == []
        command = Command("flacid")
        command.allow_user("artmattdank")
        assert command.users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]

    def test_add_street_cred(self, user):
        subject = user("artmattdank")
        assert subject.street_cred() == 0
        subject.add_street_cred()
        assert subject.street_cred() == 1

    @pytest.mark.skip
    def test_remove_all_commands(self, user):
        subject = user("artmattdank")
        assert subject.commands() == []
        command = Command("flacid")
        command.allow_user("artmattdank")
        assert command.permitted_users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]
        subject.remove_all_commands()
        assert subject.commands() == []
        assert command.permitted_users() == []
