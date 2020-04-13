from pathlib import Path

from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary


def remove_completed_requests():
    soundeffect_names = SoundeffectsLibrary.fetch_soundeffect_names()
    print(f"\n\n{soundeffect_names}\n\n")
    soundeffect_requests = Path(__file__).parent.parent.joinpath(".requests")

    unfulfilled_requests = [
        request
        for request in soundeffect_requests.read_text().strip().split("\n")
        if request.split()[3] not in soundeffect_names
    ]

    print(f"\n\nUnfulfilled Request: {unfulfilled_requests}\n\n")
    with open(soundeffect_requests, "w") as f:
        if unfulfilled_requests:
            f.write("\n".join(unfulfilled_requests) + "\n")
        else:
            f.write("")



# This belongs somewhere else
def handle_user_requests(self):
    try:
        remove_completed_requests()
    except Exception as e:
        print(f"Error Removing Message: {e}")

    soundeffect_requests = Path(__file__).parent.parent.joinpath(".requests")
    previous_requests = soundeffect_requests.read_text().split("\n")

    if previous_requests:
        for sound_request in previous_requests:
            if sound_request:
                send_twitch_msg("Request: " + sound_request)
    else:
        send_twitch_msg("No Requests! Great Job STREAM_LORDS")

