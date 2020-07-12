import pytest

from chat_thief.irc_msg import IrcMsg


class TestIrcMsg:
    def test_parsing_irc_msg(self):
        raw_msg = ":beginbot!beginbot@beginbot.tmi.twitch.tv PRIVMSG #beginbot :hello"
        subject = IrcMsg(raw_msg)
        assert subject.user == "beginbot"
        assert subject.msg == "hello"
        assert not subject.is_command()
        assert subject.command is None
        assert subject.args == []

    def test_parsing_command_msg(self):
        raw_msg = ":beginbot!beginbot@beginbot.tmi.twitch.tv PRIVMSG #beginbot :!clap"
        subject = IrcMsg(raw_msg)
        assert subject.user == "beginbot"
        assert subject.msg == "!clap"
        assert subject.is_command()
        assert subject.command == "clap"
        assert subject.args == []

    def test_parsing_command_msg_with_args(self):
        raw_msg = ":beginbot!beginbot@beginbot.tmi.twitch.tv PRIVMSG #beginbot :!add_perm clap fakeuser"
        subject = IrcMsg(raw_msg)
        assert subject.user == "beginbot"
        assert subject.msg == "!add_perm clap fakeuser"
        assert subject.is_command()
        assert subject.command == "add_perm"
        assert subject.args == ["clap", "fakeuser"]

    def test_parsing_new_soundeffect_request(self):
        raw_msg = ":beginbot!beginbot@beginbot.tmi.twitch.tv PRIVMSG #beginbot :!soundeffect Mv0oYS-qMcQ update 0:00 0:01"
        subject = IrcMsg(raw_msg)
        assert subject.user == "beginbot"
        assert subject.msg == "!soundeffect Mv0oYS-qMcQ update 0:00 0:01"
        assert subject.is_command()
        assert subject.command == "soundeffect"
        assert subject.args == ["Mv0oYS-qMcQ", "update", "0:00", "0:01"]

    def test_parsing_mixed_case_command(self):
        raw_msg = ":beginbot!beginbot@beginbot.tmi.twitch.tv PRIVMSG #beginbot :!Me"
        subject = IrcMsg(raw_msg)
        assert subject.user == "beginbot"
        assert subject.msg == "!Me"
        assert subject.is_command()
        assert subject.command == "me"
        assert subject.args == []
