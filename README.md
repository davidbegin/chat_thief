# Twitch Python Chat bot that also manages a Command Economy

This started as a simple twitch chatbot, but has evolved into a Soundboard
economy manager (More Details Below).

## What Is Going On During Your Stream

There are over 1300+ Soundeffects (added by users like you!), that area access
through various commands, like: `!clap` or `!wow`

When you join the stream you have access to no sounds (except your theme song,
if you have one). To get access to soundeffects, you just need to participate in
our New Economy!

## Participating in the Stream

### Write CSS

!css URL_TO_RAW_CSS

Pastebin
or Gitlab Snippets work great!

### Write a Bot

Write **1** Bot in whatever language, to interact with the stream, potentially
participate in Bot Survivor

### Write a JS Widget (restrictions apply)

- 25 Lines
- Vanilla

### Add Sounds to the Stream

!soundeffect YOUTUBE_URL command_name 00:00 00:04

### Get Access to Sounds By Chatting

!me
!props
!buy

---

## New Economy

**2 Types of Currency:**

### Street Cred

- You earn it from working (if you are chatting, you will earn street cred
  automatically (note: this is different than Beginbux AKA channel points)
- You can only give it to other viewer:
  `!props other_user`
  `!endorse other_user`
  `!bigups other_user`
- You may also share one of your sounds with another viewer for 1 Street Cred:
  `!share sound other_user`
- You can also transfer a soundeffect to another user, costing No Streed Cred:
  `!transfer sound other_user`

### Cool Points

- When someone gives you Street Cred, it becomes Cool Points
- Cool Points are NOT transferable
- Cool Points can be spent to buy sounds:
  `!buy clap`
  `!buy random`

## The Government

- We will not provide services to trade commands
  if you need that, then the market should supply it

## Drops

There are also random drops, when a random user is given a random sound, maybe
it will be you! You will be notified in the chat, if you receive a random item.

## Gambling

## FAQ

Q: How do you get street cred?
A: Chatting

Q: What is the difference in transfer, share, endorse, buy?
A:

- !transfer -> Transfer access to a soundeffect to another user (No Street
  Cred Required)
- !share    -> Share a sound with a User for Street Cred
- !endorse  -> Give someone your Street Cred (they become Cool Points)
- !buy      -> Purchase access to a sound with Cool Points

## Theme Song

Finally you can submit a theme song, and this is a sound that only you will have
access to. It will also play everytime you join the chat for the first time each
stream! The theme should be no more than 5 seconds from a youtube clip in the
following format:

`!soundeffect YOUTUBE_ID your_twitch_user name 00:05 00:09`

Once a Streamlord approves this, you and you alone will have access to your
theme song. It will also play everytime you say something in the chat for the
first time that stream!

## Revolution

If you accure 100 Cool Points, you can reset the entire econonmy with
`!revolution`

## Some Useful Commands

Check your own permissions
`!perms`

Check your Points:
`!me`

Check who is allowed to use !clap
`!perms clap`

Check beginbot's permissions
`!perms beginbot`

Give a command to another user
`!give command other_user`
OR
`!share command other_user`

Check the soundboard leaderboard
`!leaderboard`

Show the Streamlords
`!streamlords`

---

## Bots in Action

```bash
# Main Bot collect and responding to chat commands
python bot.py

# Bot that will read out soundeffect requests from a file
# And try to make them available
python soundeffect_request_bot.py

# Bot that will read out soundeffects from a file and play them
python soundboard_bot.py

# Bot that runs and give active chatters Street Cred on a regular basis
python street_cred_bot.py

# For testing
python fake_bot.py -m "\!clap" -u beginbotbot
```

## Exposing User Data

<https://mygeoangelfirespace.city/>
