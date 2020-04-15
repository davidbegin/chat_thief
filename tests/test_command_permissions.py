from pathlib import Path

import pytest

from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.command_permissions import CommandPermissionCenter


class TestCommandPermissions:
    db_filepath = Path(__file__).parent.joinpath("db/test.json")

    @classmethod
    def setup_class(cls):
        if cls.db_filepath.is_file():
            cls.db_filepath.unlink()

    @pytest.fixture
    def command_permission_center(self):
        def _command_permission_center(user, command, args=[]):
            return CommandPermissionCenter(
                user=user,
                command=command,
                args=args,
                db_location=self.__class__.db_filepath,
                skip_validation=True,
            )

        return _command_permission_center

    def test_adding_a_permission(self, command_permission_center):
        user = "fakeuser"
        command = "fakecommand"

        subject = command_permission_center(
            user="beginbot", command=command, args=[command, user]
        )

        initial_perms = subject.fetch_command_permissions()
        assert user not in initial_perms
        subject._add_permission()
        subject = command_permission_center(
            user=user, command=command, args=[command, user]
        )
        final_perms = subject.fetch_command_permissions()
        assert user in final_perms

    def test_checking_user_permissions(self, command_permission_center):
        user = "new_fakeuser"
        command = "fakecommand"

        subject = command_permission_center(
            user=user, command=command, args=[command, user]
        )

        allowed_commands = subject.fetch_user_permissions()
        assert allowed_commands == []

        subject._add_permission()
        allowed_commands = subject.fetch_user_permissions()
        assert allowed_commands == [command]
