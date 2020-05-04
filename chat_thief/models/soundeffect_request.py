from collections import Counter

from tinydb import Query

from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.models.database import db_table
from chat_thief.sample_saver import SampleSaver


class SoundeffectRequest:
    table_name = "soundeffect_requests"
    database_folder = ""
    database_path = "db/soundeffect_requests.json"

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def unapproved_count(cls):
        return len(cls.unapproved())

    @classmethod
    def unapproved(cls):
        return cls.db().search(Query().approved == False)

    @classmethod
    def stats(cls):
        results = cls.unapproved()
        user_stats = Counter([request["requester"] for request in results])

    @classmethod
    def count(cls):
        return len(cls.db().all())

    @classmethod
    def pop_all_off(cls):
        results = cls.db().search(Query().approved == True)
        return cls._save_samples(results, "beginbotbot")

    @classmethod
    def approve_all_for_user(cls, approver, requester):
        results = cls.db().search(Query().requester == requester)
        return cls._save_samples(results, approver)

    @classmethod
    def _save_samples(cls, results, approver):
        if results:
            print(f"\nResults: {results}")

        doc_ids_to_delete = [sfx.doc_id for sfx in results]
        if doc_ids_to_delete:
            from tinyrecord import transaction

            with transaction(cls.db()) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)

        for sfx in results:
            cls._save_sample(sfx, approver)

    @classmethod
    #  I pass in an SFX
    # Sometimes the approver, will be empty
    # and we want to pass it in
    def _save_sample(cls, sfx, approver=None):
        print(sfx)
        sample_saver = SampleSaver(
            user=approver,
            command=sfx["command"],
            youtube_id=sfx["youtube_id"],
            start_time=sfx["start_time"],
            end_time=sfx["end_time"],
        ).save(sfx["requester"])

    def __init__(
        self, user, command, youtube_id, start_time, end_time,
    ):
        self.user = user
        self.youtube_id = youtube_id
        self.command = command
        self.start_time = start_time
        self.end_time = end_time
        self.approved = self.is_auto_approved()
        self.approver = self.auto_approver()

    def save(self):
        results = self.db().search(Query().command == self.command)
        doc_ids_to_delete = [sfx.doc_id for sfx in results]
        if doc_ids_to_delete:
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)

        print(f"Creating New SFX Request: {self.doc()}")
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(self.doc())
        return self.doc()

    def is_auto_approved(self):
        # return self.user in STREAM_GODS
        return self.user in STREAM_LORDS

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
