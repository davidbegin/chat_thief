from pathlib import Path
import pytest

from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.issue import Issue
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.soundeffect_request import SoundeffectRequest

MODEL_CLASSES = [
    SoundeffectRequest,
    SFXVote,
    Command,
    User,
    Vote,
    CubeBet,
    Issue,
    BreakingNews,
]


class DatabaseConfig:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        for model in MODEL_CLASSES:
            model.database_folder = "tests/"
            db_path = Path(__file__).parent.parent.joinpath(model.database_path)
            if db_path.is_file():
                db_path.unlink()
        yield
