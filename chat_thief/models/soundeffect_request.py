from collections import Counter
import traceback
from datetime import datetime

from tinydb import Query  # type: ignore

from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.models.database import db_table
from chat_thief.audioworld.sample_saver import SampleSaver
from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.transaction import transaction


class SoundeffectRequest(BaseDbModel):
    table_name = "soundeffect_requests"
    database_path = "db/soundeffect_requests.json"

    @classmethod
    def get(cls, command):
        return cls.db().get(Query().command == command)

    @classmethod
    def unapproved_count(cls):
        return len(cls.unapproved())

    @classmethod
    def unapproved(cls):
        return cls.db().search(Query().approved == False)

    # This is the wrong data structure
    @classmethod
    def stats(cls):
        requests = cls.unapproved()
        stat_dict = {}
        for request in requests:
            stat_dict[request["requester"]] = {
                request.doc_id: {
                    "name": request["command"],
                    "youtube": SoundeffectRequest.format_clip(request),
                    "time": f"{request['start_time']} - {request['end_time']}",
                }
            }

        return stat_dict

    @classmethod
    def formatted_stats(cls):
        return [
            (
                f"@{user}"
                + " - Doc ID: "
                + " ".join(
                    [
                        f'{doc_id} - !{values["name"]} {values["youtube"]} {values["time"]}'
                        for (doc_id, values) in values.items()
                    ]
                )
            )
            for (user, values) in cls.stats().items()
        ]

    @staticmethod
    def format_clip(request):
        from chat_thief.utils.url_validator import is_valid_url

        clip_id = request["youtube_id"]

        pt = SoundeffectRequest.sfx_cut_time(request["start_time"])

        if is_valid_url(clip_id):
            if "youtu" in clip_id:
                if pt:
                    total_seconds = pt.second + pt.minute * 60
                    return f"{clip_id}?t={total_seconds}"
                else:
                    return clip_id

            # Assuming Twitch
            else:
                return clip_id
        else:
            if pt:
                total_seconds = pt.second + pt.minute * 60
                return f"https://youtu.be/{request['youtube_id']}?t={total_seconds}"
            else:
                return f"https://youtu.be/{request['youtube_id']}"

    @staticmethod
    def sfx_cut_time(cut_time):
        try:
            return datetime.strptime(cut_time, "%M:%S")
        except Exception as e:
            print(f"Error formatting Time: {cut_time}\n{e}")

    @classmethod
    def pop_all_off(cls):
        results = cls.db().search(Query().approved == True)
        return cls._save_samples(results, "beginbotbot")

    @classmethod
    def approve_all_for_user(cls, approver, requester):
        results = cls.db().search(Query().requester == requester)
        return cls._save_samples(results, approver)

    @classmethod
    def approve_all(cls, approver):
        results = cls.db().all()
        return cls._save_samples(results, approver)

    @classmethod
    def approve_command(cls, approver, command):
        results = cls.db().search(Query().command == command)
        return cls._save_samples(results, approver)

    @classmethod
    def approve_user(cls, approver, user):
        results = cls.db().search(Query().requester == user)
        return cls._save_samples(results, approver)

    @classmethod
    def approve_doc_id(cls, approver, doc_id):
        result = cls.db().get(doc_id=doc_id)
        if result:
            return cls._save_samples([result], approver)
        else:
            return f"Did not find Doc ID: {doc_id} to approve"

    @classmethod
    def deny_doc_id(cls, denier, doc_id):
        # We need to either rescue, or not
        # delete if they don't exist
        try:
            return cls.db().remove(doc_ids=[doc_id])
        except KeyError:
            traceback.print_exc()

    @classmethod
    def _save_samples(cls, results, approver):
        if results:
            print(f"\nResults: {results}")

        doc_ids_to_delete = [sfx.doc_id for sfx in results]
        if doc_ids_to_delete:
            print(f"Deleting the following IDs: {doc_ids_to_delete}")

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
        # We are messing up here
        sample_saver = SampleSaver(
            user=sfx["requester"],
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

            with transaction(self.db()) as tr:
                tr.remove(doc_ids=doc_ids_to_delete)

        print(f"Creating New SFX Request: {self.doc()}")

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
