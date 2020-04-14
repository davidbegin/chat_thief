import pytest

from chat_thief.request_saver import RequestSaver
from chat_thief.irc_msg import IrcMsg

# I could make a fake irc_msg, with just user and msg


class TestRequestSaver:
    def test_saving_a_request(self):
        subject = RequestSaver("beginbot", "!soundeffect Mv0oYS-qMcQ update 0:00 0:01")
        subject.save()
