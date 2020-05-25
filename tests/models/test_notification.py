import pytest

from chat_thief.models.notification import Notification

from tests.support.database_setup import DatabaseConfig


class TestNotification(DatabaseConfig):
    def test_notification(self):
        assert Notification.count() == 0
        Notification("Cool Stuff").save()
        assert Notification.count() == 1

        notification = Notification.last()
        assert notification["duration"] == 1
