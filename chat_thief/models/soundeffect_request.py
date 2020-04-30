from tinydb import Query

from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS

from chat_thief.models.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH
from chat_thief.sample_saver import SampleSaver


class SoundeffectRequest:
    def __init__(
        self,
        user,
        command,
        youtube_id,
        start_time,
        end_time,
        soundeffect_request_db_path="db/soundeffect_requests.json",
    ):
        self.user = user
        self.youtube_id = youtube_id
        self.command = command
        self.start_time = start_time
        self.end_time = end_time
        self.approved = self.is_auto_approved()
        self.approver = self.auto_approver()
        self.sfx_requests_db = db_table(
            soundeffect_request_db_path, "soundeffect_requests"
        )

    def save(self):
        print(f"Creating New SFX Request: {self.doc()}")
        from tinyrecord import transaction

        with transaction(self.sfx_requests_db) as tr:
            tr.insert(self.doc())
        return self.doc()

    def is_auto_approved(self):
        return self.user in STREAM_GODS
        # return self.user in STREAM_LORDS

    def auto_approver(self):
        if self.is_auto_approved():
            return self.user

    def doc(self):
        return {
            "requester": self.user,
            "approver": self.approver,
            "approved": self.approved,
            "youtube_id": self.youtube_id,
            "command": self.command,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    def approve_all_for_user(self, approver, requester):
        results = self.sfx_requests_db.search(Query().requester == requester)
        return self._save_samples(results, approver)

    def _save_samples(self, results, approver):
        if results:
            print(f"\nResults: {results}")

        doc_ids_to_delete = [sfx.doc_id for sfx in results]
        if doc_ids_to_delete:
            print(f"Doc IDs being deleted: {doc_ids_to_delete}")
            from tinyrecord import transaction

            with transaction(self.sfx_requests_db) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)

        for sfx in results:
            print(sfx)
            # Pull out beginbotbot
            sample_saver = SampleSaver(
                user=approver,
                command=sfx["command"],
                youtube_id=sfx["youtube_id"],
                start_time=sfx["start_time"],
                end_time=sfx["end_time"],
            )
            sample_saver.save(sfx["requester"])

    def pop_all_off(self):
        results = self.sfx_requests_db.search(Query().approved == True)

        if results:
            print(f"\nResults: {results}")

        doc_ids_to_delete = [sfx.doc_id for sfx in results]
        if doc_ids_to_delete:
            print(f"Doc IDs being deleted: {doc_ids_to_delete}")
        self.sfx_requests_db.remove(doc_ids=doc_ids_to_delete)

        for sfx in results:
            print(sfx)
            sample_saver = SampleSaver(
                user=sfx["approver"],
                command=sfx["command"],
                youtube_id=sfx["youtube_id"],
                start_time=sfx["start_time"],
                end_time=sfx["end_time"],
            )
            sample_saver.save(sfx["requester"])
