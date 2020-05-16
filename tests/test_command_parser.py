from chat_thief.command_parser import CommandParser

from tests.support.database_setup import DatabaseConfig


# Test Driven Development:
# End-To-End
# Acceptance Tests
#
# What is the definition of a unit test
class TestCommandParser(DatabaseConfig):
    def test_issue_with_no_info(self):
        pass
