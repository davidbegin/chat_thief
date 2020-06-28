from abc import ABC
import abc

from chat_thief.chat_parsers.command_parser import CommandParser


# Routers are for Pairing a Parser Class
class BaseRouter(ABC):
    def __init__(self, user, command, args=[], parser=None):
        self.user = user
        self.command = command
        self.args = args

        if parser:
            self.parser = parser
        else:
            self.parser = CommandParser(
                user=self.user, command=self.command, args=self.args
            ).parse()

    @abc.abstractmethod
    def route(self):
        """Take a Command and route to appropriate code"""
