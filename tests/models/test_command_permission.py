import pytest

from chat_thief.models.command_permission import CommandPermission

class TestCommandPermission:

    def test_no_more_health(self):
        user = "fake_user"
        command = "clap"
        subject = CommandPermission(
            user=user,
            command=command,
            permitted_users=[]
        )
        assert subject.health == 5
