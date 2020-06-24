import pytest

from chat_thief.audioworld.request_saver import RequestSaver
from chat_thief.irc_msg import IrcMsg

from tests.support.database_setup import DatabaseConfig

# We need to make the twitch commands configurable, or just return messages brah
# We should have twitch in there
class TestRequestSaver(DatabaseConfig):
    def test_saving_a_request(self):
        subject = RequestSaver("beginbot", "!soundeffect Mv0oYS-qMcQ update 0:00 0:01")
        subject.save()
