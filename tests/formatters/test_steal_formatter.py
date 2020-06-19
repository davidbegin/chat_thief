import pytest

from chat_thief.formatters.steal_formatter import StealFormatter
from chat_thief.new_commands.result import Result

from tests.support.database_setup import DatabaseConfig


class TestStealFormatter(DatabaseConfig):
    def test_format_successful_steal(self):
        result = Result(
            user="uzi",
            command="steal",
            metadata={
                "victim": "future",
                "target_sfx": "handbag",
                "stealing_result": "@uzi stole !handbag from @future",
            },
        )

        expected_message = "@uzi stole !handbag from @future"
        assert StealFormatter(result).format() == expected_message
