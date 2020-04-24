from pathlib import Path

import pytest

from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.audio_command import AudioCommand

commands_db_path = Path(__file__).parent.joinpath("db/commands.json")


class TestCommandPermissions:
    @pytest.fixture(autouse=True)
    def clear_db(cls):
        if commands_db_path.is_file():
            commands_db_path.unlink()

    @pytest.fixture
    def command_permission_center(self):
        def _command_permission_center(user, command):
            return PermissionsFetcher(
                user=user,
                command=command,
                commands_db_path=commands_db_path,
                skip_validation=True,
            )

        return _command_permission_center

    def test_checking_user_permissions(self, command_permission_center):
        user = "new_fakeuser"
        command = "wow"

        subject = command_permission_center(user=user, command=command)

        allowed_commands = subject.fetch_user_permissions()
        assert allowed_commands == []

        AudioCommand(
            command, commands_db_path=commands_db_path, skip_validation=True
        ).allow_user(user)
        allowed_commands = subject.fetch_user_permissions()
        assert allowed_commands == [command]
