import itertools

import pytest

from chat_thief.bwia import BWIA
from chat_thief.models.user_event import UserEvent
from tests.support.database_setup import DatabaseConfig
import chat_thief.apps.beginworld_finance
import chat_thief.apps.economist_app
import chat_thief.apps.news_app
import chat_thief.apps.notification_app
import chat_thief.bots.forbes_bot
import chat_thief.bots.hand_of_the_market
import chat_thief.bots.new_news_bot
import chat_thief.bots.soundboard_bot
import chat_thief.bots.soundeffect_request_bot
import chat_thief.mygeoangelfirespace.syncer
import chat_thief.mygeoangelfirespace.publisher


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

    def test_find_robinscore(self):
        UserEvent(
            user="uzi", command="give", msg="!give handbag @future", result=[]
        ).save()
        UserEvent(
            user="uzi", command="give", msg="!give damn @carti ", result=[]
        ).save()
        UserEvent(
            user="uzi", command="share", msg="!share rickroll @carti ", result=[]
        ).save()
        UserEvent(
            user="uzi", command="steal", msg="!steal rickroll @carti ", result=[]
        ).save()
        UserEvent(
            user="carti", command="give", msg="!give rickroll @futre", result=[]
        ).save()
        assert BWIA.robinhood_score("uzi") == 3
        assert BWIA.robinhood_score("duzi") == 0
        assert BWIA.robinhood_score("carti") == 1
