from pathlib import Path

import pytest

from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.models.command import Command
from tests.support.database_setup import DatabaseConfig


class TestPermissionsFetcher(DatabaseConfig):
    def test_checking_user_permissions(self):
        user = "new_fakeuser"
        command = "wow"
        # This will work once we have DB setup working correctly
        # Command(command).allow_user(user)
        # allowed_commands = subject.fetch_user_permissions()
        # assert allowed_commands == [command]
