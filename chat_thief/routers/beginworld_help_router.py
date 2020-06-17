from chat_thief.routers.base_router import BaseRouter
from chat_thief.config.help_menu import HELP_COMMANDS


class BeginworldHelpRouter(BaseRouter):
    def route(self):
        if self.command == "help":
            if len(self.args) > 0:
                command = self.args[0]
                if command.startswith("!"):
                    command = command[1:]
                return HELP_COMMANDS[command]
            else:
                options = " ".join([f"!{command}" for command in HELP_COMMANDS.keys()])
                return f"Call !help with a specific command for more details: {options}"
