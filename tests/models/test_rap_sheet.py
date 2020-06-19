import pytest

from chat_thief.models.rap_sheet import RapSheet

from tests.support.database_setup import DatabaseConfig


class TestRapSheet(DatabaseConfig):
    def test_new_rap_sheet(self):
        subject = RapSheet(
            user="beginbotsmonster",
            action="caught_stealing",
            metadata={"target_sfx": "handbag", "victim": "uzi"},
        )
        assert RapSheet.count() == 0
        subject.save()
        assert RapSheet.count() == 1
