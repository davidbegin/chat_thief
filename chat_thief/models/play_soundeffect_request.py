import json
import traceback

from tinydb import Query

from chat_thief.models.database import db_table


class PlaySoundeffectRequest:
    def __init__(self, user=None, command=None):
        self.user = user
        self.command = command
        play_soundeffect_requests_db_path = "db/play_soundeffects.json"
        self.play_sfx_db = db_table(
            play_soundeffect_requests_db_path, "play_soundeffects"
        )

    def save(self):
        if self._is_valid_json():
            print(f"Play SFX Request: {self.doc()}")

            from tinyrecord import transaction

            with transaction(self.play_sfx_db) as tr:
                tr.insert(self.doc())
            return self.doc()

        else:
            return f"There was an issue with {self.doc()}"

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
        }

    def pop_all_off(self):
        all_effects = self.play_sfx_db.all()
        doc_ids_to_delete = [sfx.doc_id for sfx in all_effects]
        if doc_ids_to_delete:
            print(f"Doc IDs being deleted: {doc_ids_to_delete}")
            from tinyrecord import transaction

            with transaction(self.play_sfx_db) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)
            return all_effects
        else:
            return []
