from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.audio_player import AudioPlayer


class AudioCommand:
    def __init__(self, name):
        self.name = name
        self.soundfile = SoundeffectsLibrary.find_sample(name)
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()

    def play_sample(self):
        AudioPlayer.play_sample(self.soundfile.resolve())

    # def allowed_to_play(self, user):
    #     if user in STREAM_LORDS:
    #         return True

    #     if self.name == "clap":
    #         return True

    #     if result := self.table.search(Query().command == self.command):
    #         return result[-1]["permitted_users"]
    #     if
    #     # allowed_users = self.command_permission_center.fetch_command_permissions()
    #     if self._is_personal_theme_song() and self._is_theme_song():
    #         return [self.user]

    #     if not self._is_personal_theme_song() and self._is_theme_song():
    #         return []

    #     if self.command == "snorlax" and self.user == "artmattdank":
    #         return ["snorlax"]

    #     if self.user in STREAM_LORDS:
    #         return [self.user]

    #     if result := self.table.search(Query().command == self.command):
    #         return result[-1]["permitted_users"]
    #     else:
    #         return []
