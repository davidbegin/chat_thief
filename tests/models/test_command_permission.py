import pytest

from chat_thief.models.command_permission import CommandPermission


class TestCommandPermission:
    def test_no_more_health(self):
        CommandPermission.database_path = "dbz/commands.json"
        user = "fake_user"
        command = "clap"
        subject = CommandPermission(user=user, command=command, permitted_users=[])
        assert subject.health == 5
        # subject.database_path = "dbz/commands.json"
        assert subject.database_path == "dbz/commands.json"
        assert subject.is_healthy() == "dbz/commands.json"
        # assert subject.is_healthy()
