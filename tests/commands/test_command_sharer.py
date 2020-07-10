import pytest
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.models.user import User
from chat_thief.models.command import Command
from tests.support.database_setup import DatabaseConfig


class TestCommandSharer(DatabaseConfig):
    def test_share(self):
        user = User("fake_user")
        user.update_cool_points(1)
        command = Command("damn")
        friend = User("bizmarkie")

        command.allow_user(user.name)
        assert user.name in command.users()
        assert friend.name not in command.users()

        subject = CommandSharer(
            user=user.name, command=command.name, friend=friend.name,
        )

        subject.share()

        assert user.name in command.users()
        assert friend.name in command.users()
        assert user.cool_points() == 0
        assert command.cost() == 3

    def test_broke_boi_share(self):
        user = User("fake_user")
        command = Command("damn")
        friend = User("bizmarkie")

        command.allow_user(user.name)
        assert user.name in command.users()
        assert friend.name not in command.users()

        subject = CommandSharer(
            user=user.name, command=command.name, friend=friend.name,
        )

        subject.share()

        assert user.name in command.users()
        assert friend.name not in command.users()
        assert command.cost() == 1

    def test_invalid_command(self):
        user = User("fake_user")
        friend = User("bizmarkie")

        result = CommandSharer(
            user=user.name, command="fake_command", friend=friend.name,
        ).share()
        assert result == "@fake_user cannot share !fake_command as it's invalid"
