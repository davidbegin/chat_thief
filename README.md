# Welcome To BeginWorld™

What started as a simple idea for a chat-controlled soundboard, has evolved
into an entire economy with multiple ways of participating.

## What Is Going On During Your Stream

There are over [1300+
Soundeffects](https://github.com/davidbegin/twitch-soundboard) (added by users
like you!), that are accessible
through various commands, like:

```twitch chat
!me
!clap
!wow
```

You can: earn, trade, steal, and gamble with these sounds.

As you chat and participate in the stream you get access to more sounds by
either the friends you make in chat, strategic bets and/or investments.

## Other Ways to Participate

We like to talk about and discuss the code on stream, as well as wanting to encourage you to code too!
If you are wanting to learn about code then we are the community for you. There is multiple ways for you
to participate and also influence the stream, so stick around to discover them!

This entire system was largely influeced by Users participating themselves.

### Write CSS

Type in the Chat:

```twitch chat
!me
```

To see your page [Example Page](https://mygeoangelfirespace.city/zanuss.html)

You can style your page with:

```twitch chat
!css URL_TO_RAW_CSS
```
The 2 best options we found are:
[Pastebin](https://pastebin.com/)
[Gitlab Snippets](https://gitlab.com/snippets/new)

**Note:** Make sure to link to the raw CSS. Typically the link will have "raw"
inside of it.

On the [Homepage](https://mygeoangelfirespace.city/) you will see a Homepage CSS
Leaderboard, which lists the most popular user pages.

You can vote for your favorite page with:

```twitch chat
!bestcss @user
```

The User with the most votes, controls the styling of the homepage and all
shared pages. There is a list of all Users who have styled thier pages under "Stylish Users"
on the [Homepage](https://mygeoangelfirespace.city/)

### Write a Chat Bot

Write **1** Bot in whatever language you desire so it can then interact with the stream and
it might even participate in Bot Survivor!

You must register your bot by telling Begin and the chat who your bot is.

**If you violate the rules, you will be banned!!**

For More Details on Bots in BeginWorld see:
[Bot Law](docs/BOT_LAW.md)

### Write a JS Widget

You can write a JS widget to be used on your page,
and made available for purchase on other pages.

The restrictions are:

- 25 Lines of Code (Not minifier)
- Vanilla JS only!

We will make a "Widget Shop" Available, give creators
a chance to sell their Widgets.

We will make a "Widget Shop" available to give creators
a one-stop shop to sell them.

Please keep in mind that when a widget is submitted,
it has to be approved by a team of reviewers.

| Reviewers   | Approvers   |
| ----------- | ----------- |
| eno         | N/A         |

#### Why

We aim to simulate the smallest market for selling code.
This will help members learn to code and give them a goal
to work towards.

### Add Sounds to the Stream

```twitch chat
!soundeffect YOUTUBE_URL command_name 00:00 00:04
```

[Youtube-DL](https://github.com/ytdl-org/youtube-dl)

### Get Access to Sounds By Chatting

!me
!props
!buy

---

## New Economy

**2 Types of Currency:**

### Street Cred

- You earn it from working (if you are chatting, you will earn street cred
  automatically **note: this is different than Beginbux AKA channel points**)
- You can only give it to other viewers:
  `!props other_user`
  `!endorse other_user`
  `!bigups other_user`
- You may also share one of your sounds with another viewer for 1 Street Cred:
  `!share sound other_user`
- You can also transfer a soundeffect to another user, costing **No** Streed Cred:
  `!transfer sound other_user`

### Cool Points

- When someone gives you Street Cred, it becomes Cool Points
- Cool Points are NOT transferable
- Cool Points can be spent to buy sounds:
  `!buy clap`
  `!buy random`

## The Government

- We will not provide services to trade commands
  if you need that, then the market should supply it.

## Drops

There are also random drops, when a random user is given a random sound, maybe
it will be you! You will be notified in the chat, if you receive a random item.

## Gambling

## FAQ

Q: How do you get street cred?
A: Chatting

Q: What is the difference in transfer, share, endorse, buy?
A:
| Command     | Description |
| ----------- | ----------- |
| !transfer   | Transfer access to a soundeffect to another user (No Street Cred Required) |
| !share      | Share a sound with a User for Street Cred                                  |
| !endorse    | Give someone your Street Cred (they become Cool Points)                    |
| !buy        | Purchase access to a sound with Cool Points                                |

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

If you accure 100 Cool Points, you can reset the entire econonmy with:
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

## Website

<https://mygeoangelfirespace.city/>
