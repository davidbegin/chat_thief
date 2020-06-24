from pathlib import Path

from chat_thief.irc import send_twitch_msg
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary

SOUNDEFFECT_REQUESTS_PATH = Path(__file__).parent.parent.parent.joinpath("db/.requests")


def _remove_completed_requests():
    soundeffect_names = SoundeffectsLibrary.fetch_soundeffect_names()

    unfulfilled_requests = [
        request
        for request in SOUNDEFFECT_REQUESTS_PATH.read_text().strip().split("\n")
        if request.split()[3] not in soundeffect_names
    ]

    print(f"\n{soundeffect_names}\n")
    print(f"\n\nUnfulfilled Request: {unfulfilled_requests}\n\n")
    with open(SOUNDEFFECT_REQUESTS_PATH, "w") as f:
        if unfulfilled_requests:
            f.write("\n".join(unfulfilled_requests) + "\n")
        else:
            f.write("")


def handle_user_requests():
    previous_requests = [
        request
        for request in SOUNDEFFECT_REQUESTS_PATH.read_text().split("\n")
        if request != ""
    ]

    print(f"Previous Requests: {previous_requests}")

    if previous_requests:
        for sound_request in previous_requests:
            if sound_request:
                send_twitch_msg("Request: @" + sound_request)
    else:
        send_twitch_msg("No Requests! Great Job STREAM_LORDS")

    try:
        _remove_completed_requests()
    except Exception as e:
        print(f"Error Removing Message: {e}")
