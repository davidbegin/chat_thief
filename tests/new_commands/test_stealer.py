import random

import pytest

from tests.support.database_setup import DatabaseConfig
from chat_thief.new_commands.stealer import Stealer
from chat_thief.new_commands.result import Result
from chat_thief.models.command import Command
from chat_thief.models.user import User


class TestStealer(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def control_chaos(self):
        random.seed(0)

    def test_stealing(self):
        madonna = User("madonna")
        bowie = User("bowie")
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        assert "handbag" not in madonna.commands()
        assert "handbag" in bowie.commands()
        result = subject.steal()
        assert isinstance(result, Result)
        assert "handbag" in madonna.commands()
        assert "handbag" not in bowie.commands()
        assert madonna.mana() == 1
        result.metadata["stealing_result"] == "@madonna stole from @bowie"

    def test_trying_to_steal_sound_you_do_not_own(self):
        madonna = User("madonna")
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

    def test_caught_stealing(self):
        random.seed(5)
        madonna = User("madonna")
        bowie = User("bowie")
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        assert madonna.mana() == 3
        assert "handbag" not in madonna.commands()
        assert "handbag" in bowie.commands()
        result = subject.steal()
        assert "handbag" not in madonna.commands()
        assert "handbag" in bowie.commands()
        assert isinstance(result, Result)
        assert madonna.mana() == 0
        assert (
            "@madonna WAS CAUGHT STEALING! Chance of Success:"
            in result.metadata["stealing_result"]
        )

    def test_no_mana_to_steal(self):
        madonna = User("madonna")
        madonna.set_value("mana", 0)
        bowie = User("bowie")
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        result = subject.steal()
        assert (
            result.metadata["stealing_result"]
            == "@madonna has no Mana to steal from @bowie"
        )

    def test_successful_steal_from_a_rich_person(self):
        random.seed(1)
        madonna = User("madonna")
        madonna.set_value("cool_points", 1)
        bowie = User("bowie")
        bowie.set_value("cool_points", 10)
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        result = subject.steal()
        assert (
            result.metadata["stealing_result"]
            == "@madonna stole from @bowie. Chance of Success: 39%"
        )

    def test_stole_from_a_rich_person(self):
        random.seed(1)
        madonna = User("madonna")
        madonna.set_value("cool_points", 1)
        bowie = User("bowie")
        bowie.set_value("cool_points", 10)
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        result = subject.steal()
        assert (
            result.metadata["stealing_result"]
            == "@madonna stole from @bowie. Chance of Success: 39%"
        )

    def test_stealing_from_an_insured_person(self):
        random.seed(0)
        madonna = User("madonna")
        madonna.set_value("cool_points", 1)
        bowie = User("bowie")
        bowie.set_value("cool_points", 10)
        bowie.buy_insurance()
        assert bowie.insured()
        handbag = Command("handbag").save().allow_user("bowie")
        subject = Stealer(thief="madonna", target_sfx="handbag", victim="bowie")
        result = subject.steal()
        assert (
            result.metadata["stealing_result"]
            == f"@madonna was blocked by @bowie's insurance! Num Attempts: 0"
        )
        assert not bowie.insured()
