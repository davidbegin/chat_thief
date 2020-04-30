from pathlib import Path

import pytest

from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.permissions_manager import PermissionsManager
from chat_thief.models.command import Command
from chat_thief.models.user import User


commands_db_path = Path(__file__).parent.parent.joinpath(Command.database_path)
Command.database_folder = "tests/"

class TestPermissionsManager:
    @pytest.fixture(autouse=True)
    def clear_db(self):
        if commands_db_path.is_file():
            commands_db_path.unlink()

    @pytest.fixture
    def permissions_manager(self):
        def _permissions_manager(user, command, target_user, target_command):
            return PermissionsManager(
                user=user,
                command=command,
                target_user=target_user,
                target_command=target_command,
            )

        return _permissions_manager

    def test_adding_a_permission(self, permissions_manager):
        user = "fakeuser"
        command = "yaboi"

        subject = permissions_manager(
            user="beginbot", command=command, target_user=user, target_command=command
        )

        # initial_perms = Command(command).users()
        # Command(command).allow_user(user)
        # assert user not in initial_perms
        # subject = permissions_manager(
        #     user=user, command=command, target_user=user, target_command=command
        # )

        # final_perms = audio_command.permitted_users()
        # assert user in final_perms

    def test_checking_user_permissions(self, permissions_manager):
        user = "fakeuser_3"
        command = "damn"

        subject = permissions_manager(
            user=user, command=command, target_user=user, target_command=command
        )
