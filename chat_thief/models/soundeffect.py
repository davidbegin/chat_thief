from dataclasses import dataclass
from typing import List


@dataclass
class SoundEffect:
    user: str
    youtube_id: str
    name: str
    start_time: str
    end_time: str
