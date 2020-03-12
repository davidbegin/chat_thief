import os
from dataclasses import dataclass

DEFAULT_BOT = "beginbotbot"
DEFAULT_CHANNEL = "zabt2"
# DEFAULT_CHANNEL = "beginbotbot"

@dataclass
class TwitchConfig:
    token: str = os.environ["TWITCH_OAUTH_TOKEN"]
    bot: str = os.environ.get("TWITCH_BOT_NAME", DEFAULT_BOT)
    channel: str=os.environ.get("TWITCH_CHANNEL", DEFAULT_CHANNEL)

    def __repr__(self):
        return f"TwitchConfig(bot: {self.bot}, channel: {self.channel})"

