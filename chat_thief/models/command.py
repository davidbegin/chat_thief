from tinydb import Query

from chat_thief.models.database import db_table
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_GODS


class Command:
    table_name = "commands"
    database_folder = ""
    database_path = "db/commands.json"

    # name is the name of the command
    # typically corresponding to a sample stored on my computer
    def __init__(self, name):
        self.name = name
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def allowed_to_play(self, user):
        if self.is_theme_song:
            return user == self.name

        if user in STREAM_GODS:
            return True

        if command := self.db().get(Query().command == self.name):
            return user in command["permitted_users"]

        return False
