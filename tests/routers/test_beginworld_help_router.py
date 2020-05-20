import pytest

from chat_thief.routers.beginworld_help_router import BeginworldHelpRouter


class TestBeginworldHelpRouter:
    def test_help_with_no_commands(self):
        result = BeginworldHelpRouter("beginbotbot", "help").route()
        assert "Call !help with a specific command for more details:" in result
