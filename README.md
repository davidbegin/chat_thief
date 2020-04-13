# Simple Python Twitch Chat Client with no deps

Set the following environment variables:

- TWITCH_OAUTH_TOKEN
- TWITCH_CHANNEL
- TWITCH_BOT_NAME

```bash
python bot.py

python fake_bot.py

python art.py
```

## Goals

- I want chat_thief to be unix-like:
  - Send messages to chat
  - Collect messages and send them somewhere

```bash
# Sends message to Twitch
beginbot

# Pulls message Chat
beginchat
```

## Vim Integration

We want a command that takes the selected area and sends it the command
