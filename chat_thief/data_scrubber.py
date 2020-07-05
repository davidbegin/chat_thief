from tinydb import Query  # type: ignore

from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary


class DataScrubber:
    @staticmethod
    def purge_duplicates():
        for cmd in Command.db().all():
            results = Command.db().search(Query().name == cmd["name"])
            if len(results) > 1:
                unflatted_permitted_users = [
                    result["permitted_users"] for result in results
                ]
                permitted_users = list(
                    set(
                        [
                            item
                            for sublist in unflatted_permitted_users
                            for item in sublist
                        ]
                    )
                )

                first, *duplicates = results
                Command.db().update(
                    {"permitted_users": permitted_users}, doc_ids=[first.doc_id]
                )
                doc_ids = [dup.doc_id for dup in duplicates]
                Command.db().remove(doc_ids=doc_ids)

    @staticmethod
    def purge_theme_songs():
        themes = SoundeffectsLibrary.fetch_theme_songs()

        to_delete = []
        for cmd in Command.db().all():
            name = cmd["name"]
            if name in themes:

                print(f"ILLEGAL COMMAND: {name}")
                command = Command(name)
                illegal_users = command.users()
                for user in illegal_users:
                    command.unallow_user(user)
                to_delete.append(cmd.doc_id)
        Command.delete(to_delete)

    @staticmethod
    def purge_duplicate_users():
        found_users = []
        to_delete = []

        for user in User.db().all():
            if user["name"] not in found_users:
                found_users.append(user["name"])
            else:
                print(f"TO DELETE: {user['name']}")
                to_delete.append(user.doc_id)

        print(f"IDS TO DELETE: {to_delete}")
