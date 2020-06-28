import pytest

from chat_thief.models.user_code import UserCode
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig


class TestUserCode(DatabaseConfig):
    def test_user_code(self):
        assert UserCode.count() == 0

        UserCode(
            user="eno", code_link="https://gitlab.com/real_url/begin.js", code_type="js"
        ).save()

        last = UserCode.last()
        assert last["approved"] == False

        # Tier 2 and 3 Get more
        # And they nerfed Tier 1
