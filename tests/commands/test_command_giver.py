import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.commands.command_giver import CommandGiver

from tests.support.database_setup import DatabaseConfig


class TestCommandGiver(DatabaseConfig):
    def test_giving_a_command(self):
        user = User("Miles")
        friend = User("Coltrane")
        command = Command("damn")
        command.allow_user(user.name)

        assert user.name in command.users()
        assert friend.name not in command.users()

        subject = CommandGiver(user=user.name, command=command.name, friend=friend.name)
        subject.give()

        assert user.name not in command.users()
        assert friend.name in command.users()

    def test_giving_a_command_unallowed_command(self):
        user = User("Miles")
        friend = User("Coltrane")
        command = Command("damn")

        assert user.name not in command.users()
        assert friend.name not in command.users()

        subject = CommandGiver(user=user.name, command=command.name, friend=friend.name)
        subject.give()

        assert user.name not in command.users()
        assert friend.name not in command.users()

    def test_giving_a_command_to_yourself(self):
        user = User("Miles")
        command = Command("damn")
        command.allow_user(user.name)

        assert user.name in command.users()

        with pytest.raises(ValueError) as e:
            subject = CommandGiver(
                user=user.name, command=command.name, friend=user.name
            )
            subject.give()
