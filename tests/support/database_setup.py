from pathlib import Path
import pytest

from chat_thief.models.base_db_model import BaseDbModel
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.command import Command
from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.issue import Issue
from chat_thief.models.notification import Notification
from chat_thief.models.proposal import Proposal
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.models.cube_stats import CubeStats
from chat_thief.models.the_fed import TheFed
from chat_thief.models.user_event import UserEvent
from chat_thief.models.rap_sheet import RapSheet
from chat_thief.models.bot_vote import BotVote
from chat_thief.models.tribal_council import TribalCouncil
from chat_thief.models.css_vote import CSSVote
from chat_thief.models.user_code import UserCode
from chat_thief.models.user_page import UserPage

MODEL_CLASSES = [
    BreakingNews,
    Command,
    CubeBet,
    CSSVote,
    CubeStats,
    Issue,
    Notification,
    PlaySoundeffectRequest,
    Proposal,
    RapSheet,
    SFXVote,
    SoundeffectRequest,
    TheFed,
    User,
    UserEvent,
    UserPage,
    Vote,
    BotVote,
    TribalCouncil,
    UserCode,
]


class DatabaseConfig:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        BaseDbModel.database_folder = "tests/"

        for model in MODEL_CLASSES:
            model.database_folder = "tests/"
            db_path = Path(__file__).parent.parent.joinpath(model.database_path)
            if db_path.is_file():
                db_path.unlink()
        yield
