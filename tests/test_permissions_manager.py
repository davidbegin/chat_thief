from pathlib import Path

import pytest

from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.permissions_manager import PermissionsManager
from chat_thief.audio_command import AudioCommand
from chat_thief.user import User


class TestPermissionsManager:
    db_filepath = Path(__file__).parent.joinpath("db/test.json")

    @classmethod
    def setup_class(cls):
        if cls.db_filepath.is_file():
            cls.db_filepath.unlink()

    @pytest.fixture
    def permissions_manager(self):
        def _permissions_manager(user, command, args=[]):
            return PermissionsManager(
                user=user,
                command=command,
                args=args,
                db_location=self.__class__.db_filepath,
                skip_validation=True,
            )

        return _permissions_manager

    def test_adding_a_permission(self, permissions_manager):
        user = "fakeuser"
        command = "yaboi"

        subject = permissions_manager(
            user="beginbot", command=command, args=[command, user]
        )

        audio_command = AudioCommand(
            command, skip_validation=True, db_location=self.__class__.db_filepath
        )

        initial_perms = audio_command.permitted_users()

        assert user not in initial_perms
        audio_command.allow_user(user)
        subject = permissions_manager(user=user, command=command, args=[command, user])
        final_perms = audio_command.permitted_users()
        assert user in final_perms

    def test_checking_user_permissions(self, permissions_manager):
        user = "fakeuser_3"
        command = "damn"

        subject = permissions_manager(user=user, command=command, args=[command, user])

        allowed_commands = User(user, db_location=self.__class__.db_filepath).commands()
        assert allowed_commands == []

        audio_command = AudioCommand(
            command, skip_validation=True, db_location=self.__class__.db_filepath
        )

        audio_command.allow_user(user)

        allowed_commands = User(user, db_location=self.__class__.db_filepath).commands()
        final_perms = audio_command.permitted_users()
        assert allowed_commands == [command]
