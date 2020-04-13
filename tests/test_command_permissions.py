from pathlib import Path

import pytest

from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.command_permissions import CommandPermissionCenter


class TestCommandPermissions:
    db_filepath = Path(__file__).parent.joinpath("db/test.json")

    @classmethod
    def setup_class(cls):
        cls.db_filepath.unlink()

    @pytest.fixture
    def subject(self):
        return CommandPermissionCenter(self.__class__.db_filepath)

    def test_adding_a_permission(self, subject):
        user = "fakeuser"
        command = "fakecommand"

        initial_perms = subject.fetch_command_permissions(command)
        assert user not in initial_perms
        subject.add_permission("beginbot: " + command + " " + user)
        final_perms = subject.fetch_command_permissions(command)
        assert user in final_perms

    def test_checking_user_permissions(self, subject):
        user = "new_fakeuser"
        command = "fakecommand"

        allowed_commands = subject.fetch_user_permissions(user)
        assert allowed_commands == []
        subject.add_permission(f"{user}: " + command + " " + user)
        allowed_commands = subject.fetch_user_permissions(user)
        assert allowed_commands == [command]
