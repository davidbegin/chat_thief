
def shoutout(msg) -> str:
    msg_segs = msg.split()

    if len(msg_segs) > 1 and msg_segs[1].startswith("@"):
        return f"Shoutout twitch.tv/{msg_segs[1][1:]}"
    else:
        return f"Shoutout twitch.tv/{msg_segs[1]}"
