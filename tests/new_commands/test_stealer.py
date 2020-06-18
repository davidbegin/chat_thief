# import pytest

# from tests.support.database_setup import DatabaseConfig
# from chat_thief.new_commands.stealer import Stealer
# from chat_thief.new_commands.result import Result
# from chat_thief.models.command import Command
# from chat_thief.models.user import User


# class TestStealer(DatabaseConfig):
#     def test_stealing(self):
#         subject = Stealer(user="madonna", target_sfx="handbag", victim="bowie")
#         result = subject.steal()
#         assert isinstance(result, Result)
