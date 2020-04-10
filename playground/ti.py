from tinydb import TinyDB, Query
from dataclasses import dataclass

db = TinyDB('db/soundeffects.json')
soundeffects_table = db.table("soundeffects")
SoundEffectQuery = Query()

# @dataclass
# class SoundEffect:
#     viewer: str
#     youtube_id: str
#     name: str
#     start_time: str
#     end_time: str

# sound = SoundEffect(
#     viewer="beginbot",
#     youtube_id="Mv0oYS-qMcQ",
#     name="update",
#     start_time="0:00",
#     end_time="0:01",
# )

def fetch_by_command(command):
    return soundeffects_table.search(SoundEffectQuery.name == command)

def fetch_by_viewer(viewer):
    return soundeffects_table.search(SoundEffectQuery.viewer == viewer)

print(fetch_by_command("update"))
print(fetch_by_viewer("beginbot"))
