import itertools

import pytest

from chat_thief.bwia import BWIA
from chat_thief.models.user_event import UserEvent
from tests.support.database_setup import DatabaseConfig


class TestBWIA(DatabaseConfig):
    def test_thieves(self):
        UserEvent(
            user="uzi", command="steal", msg="!steal handbag @future", result=[]
        ).save()
        UserEvent(
            user="uzi", command="steal", msg="!steal damn @carti ", result=[]
        ).save()
        UserEvent(
            user="carti", command="steal", msg="!steal rickroll @futre", result=[]
        ).save()
        assert BWIA.thieves() == [("uzi", 2), ("carti", 1)]

    def test_find_thief(self):
        UserEvent(
            user="uzi", command="steal", msg="!steal handbag @future", result=[]
        ).save()
        UserEvent(
            user="uzi", command="steal", msg="!steal damn @carti ", result=[]
        ).save()
        UserEvent(
            user="carti", command="steal", msg="!steal rickroll @futre", result=[]
        ).save()
        assert BWIA.find_thief("uzi") == 2
        assert BWIA.find_thief("duzi") == 0
