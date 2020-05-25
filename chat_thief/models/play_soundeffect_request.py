import json
import traceback

from tinydb import Query

from chat_thief.models.database import db_table
from chat_thief.models.base_db_model import BaseDbModel


class PlaySoundeffectRequest(BaseDbModel):
    table_name = "play_soundeffects"
    database_path = "db/play_soundeffects.json"

    def __init__(self, user=None, command=None, notification=True):
        self.user = user
        self.notification = notification
        if command:
            self.command = command.lower()
        play_soundeffect_requests_db_path = "db/play_soundeffects.json"
        self.play_sfx_db = db_table(
            play_soundeffect_requests_db_path, "play_soundeffects"
        )

    def command_count(self):
        # We should check if this is valid json
        return len(self.play_sfx_db)

    def _is_valid_json(self):
        try:
            json.dumps(self.doc())
            return True
        except:
            traceback.print_exc()
            return False

    def doc(self):
        return {
            "user": self.user,
            "command": self.command,
            "notification": self.notification,
        }

    def pop_all_off(self):
        from tinyrecord import transaction

        all_effects = self.play_sfx_db.all()

        doc_ids_to_delete = [sfx.doc_id for sfx in all_effects]
        if doc_ids_to_delete:
            with transaction(self.play_sfx_db) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)
            return all_effects
        else:
            return []
