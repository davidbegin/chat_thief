from pathlib import Path

import pytest

from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.audio_command import AudioCommand

db_filepath = Path(__file__).parent.joinpath("db/commands.json")


class TestCommandPermissions:
    @classmethod
    def setup_class(cls):
        if db_filepath.is_file():
            db_filepath.unlink()

    @pytest.fixture
    def command_permission_center(self):
        def _command_permission_center(user, command, args=[]):
            return CommandPermissionCenter(
                user=user,
                command=command,
                args=args,
                db_location=db_filepath,
                skip_validation=True,
            )

        return _command_permission_center

    def test_checking_user_permissions(self, command_permission_center):
        user = "new_fakeuser"
        command = "wow"

        subject = command_permission_center(
            user=user, command=command, args=[command, user]
        )

        allowed_commands = subject.fetch_user_permissions()
        assert allowed_commands == []

        AudioCommand(command, db_location=db_filepath, skip_validation=True).allow_user(
            user
        )
        allowed_commands = subject.fetch_user_permissions()
        assert allowed_commands == [command]
