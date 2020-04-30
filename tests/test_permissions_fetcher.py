from pathlib import Path

import pytest

from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.models.command import Command

commands_db_path = Path(__file__).parent.parent.joinpath(Command.database_path)
Command.database_folder = "tests/"

class TestPermissionsFetcher:
    @pytest.fixture
    def command_permission_center(self):
        def _command_permission_center(user, command):
            return PermissionsFetcher(
                user=user
            )

        return _command_permission_center

    def test_checking_user_permissions(self, command_permission_center):
        user = "new_fakeuser"
        command = "wow"
        subject = command_permission_center(user=user, command=command)
        # This will work once we have DB setup working correctly
        # Command(command).allow_user(user)
        # allowed_commands = subject.fetch_user_permissions()
        # assert allowed_commands == [command]
