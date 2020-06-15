import pytest

# from chat_thief.models.command import Command
# from chat_thief.models.user import User
from chat_thief.models.user_event import UserEvent

from tests.support.database_setup import DatabaseConfig


# Information Commands
#   Examples:
#     - !me
#     - !perms
#
# Economy Commands
#    Examples:
#      - !buy
#      - !steal
#
#  Philanthropic Commands
#      - !donate
#      - !give
#
# Market Manipulators


class TestUserEvent(DatabaseConfig):
    def test_count(self):
        assert UserEvent.count() == 0

        subject = UserEvent(
            user="beginbot", command="me", msg="!me", result="Cool Result"
        )
        subject.save()
        assert UserEvent.count() == 1
        user_event = UserEvent.last()
        assert user_event["user"] == "beginbot"
        assert user_event["command"] == "me"
        assert "created_at" in user_event

    def test_buy(self):
        pass
