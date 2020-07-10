from typing import List, Union, Optional, Any

from abc import ABC
import abc
from chat_thief.chat_parsers.command_parser import CommandParser


# Routers are for Pairing a Parser Class
# TODO: reconsider the Any for the Parser
class BaseRouter(ABC):
    def __init__(
        self,
        user: str,
        command: str,
        args: Optional[List[str]] = [],
        parser: Optional[Any] = None,
    ):
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
    def route(self) -> Optional[Union[List[str], str]]:
        """Take a Command and route to appropriate code"""
