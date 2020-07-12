import pytest

from chat_thief.chat_logs import ChatLogs


def parse_raw_irc(raw_msg):
    BEGINBOTBOT = ":beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv"
    return raw_msg.split(BEGINBOTBOT)[0].strip()


# :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv
# :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv
# :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv PRIVMSG #beginbot :!wildcard
def test_parse_raw_irc():
    irc_msg = "whatsinmyopsec: so i can be a web dever :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv PRIVMSG #beginbot :@lunchboxsushi now has access to !myspacepage :beginbotbot!beginbotbot@beginbotbot.tmi.twitch.tv PRIVMSG #beginbot :Welcome @lunchboxsushi! You need a Theme song (max 5 secs): !soundeffect YOUTUBE-URL @lunchboxsushi 00:03 00:07"
    result = parse_raw_irc(irc_msg)
    assert result == "whatsinmyopsec: so i can be a web dever"

    irc_msg = "whatsinmyopsec: so i can be a web dever"
    result = parse_raw_irc(irc_msg)
    assert result == "whatsinmyopsec: so i can be a web dever"


# This need to target other logs
@pytest.mark.skip
class TestChatLogs:
    def test_users(self):
        users = ChatLogs().users()
        assert len(users) > 10

    def test_most_msgs(self):
        msg_counts = ChatLogs().most_msgs()
        assert len(msg_counts) > 10

    def test_recent_stream_peasants(self):
        msg_counts = ChatLogs().recent_stream_peasants()
        assert msg_counts
