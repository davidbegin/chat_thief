import pytest
from chat_thief.commands.command_stealer import CommandStealer
from chat_thief.models.user import User
from chat_thief.models.command import Command
from tests.support.database_setup import DatabaseConfig


class TestCommandStealer(DatabaseConfig):
    def test_steal(self):
        thief = User("hamburgler")
        thief.update_cool_points(1)

        command = Command("mclovin")
        victim = User("grimace")
        command.allow_user(victim.name)

        assert victim.name in command.users()
        assert thief.name not in command.users()

        subject = CommandStealer(
            thief=thief.name, command=command.name, victim=victim.name,
        )

        subject.steal()

        assert thief.name in command.users()
        assert victim.name not in command.users()

        subject = CommandStealer(
            thief=thief.name, command="fake_command", victim=victim.name,
        )
        result = subject.steal()
        '@hamburgler BROKE BOI!'
