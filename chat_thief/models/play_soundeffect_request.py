import json
import traceback

from tinydb import Query  # type: ignore

from chat_thief.models.database import db_table
from chat_thief.models.transaction import transaction
from chat_thief.models.base_db_model import BaseDbModel


class PlaySoundeffectRequest(BaseDbModel):
    table_name = "play_soundeffects"
    database_path = "db/play_soundeffects.json"

    def __init__(self, user=None, command=None, notification=True):
        self.user = user
        self.notification = notification
        if command:
            self.command = command.lower()

    def __len__(self):
        return 0

    # Deprecate this
    def command_count(self):
        # We should check if this is valid json
        return self.count()

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
        all_effects = self.all()

        doc_ids_to_delete = [sfx.doc_id for sfx in all_effects]
        if doc_ids_to_delete:
            with transaction(self.db()) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)
            return all_effects
        else:
            return []
