import pytest

from tests.support.database_setup import DatabaseConfig
from chat_thief.new_commands.stealer import Stealer
from chat_thief.new_commands.result import Result
from chat_thief.models.command import Command
from chat_thief.models.user import User


class TestStealer(DatabaseConfig):
    def test_stealing(self):
        madonna = User("madonna")
        madonna.set_value("cool_points", 10)
        bowie = User("bowie")
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        assert "handbag" not in madonna.commands()
        assert "handbag" in bowie.commands()
        result = subject.steal()
        assert isinstance(result, Result)
        assert "handbag" in madonna.commands()
        assert "handbag" not in bowie.commands()

        result.metadata["stealing_result"] == "@madonna stole from @bowie"

    def test_trying_to_steal_sound_you_do_not_own(self):
        madonna = User("madonna")
        madonna.set_value("cool_points", 10)
        bowie = User("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        assert "handbag" not in madonna.commands()
        assert "handbag" not in bowie.commands()
        result = subject.steal()
        assert isinstance(result, Result)
        assert "handbag" not in madonna.commands()
        assert "handbag" not in bowie.commands()
        result.metadata[
            "stealing_result"
        ] == "@madonna failed to steal !handbag from @bowie"
