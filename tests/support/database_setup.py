from pathlib import Path
import pytest

from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.models.soundeffect_request import SoundeffectRequest

SoundeffectRequest.database_folder = "tests/"
SFXVote.database_folder = "tests/"
Command.database_folder = "tests/"
User.database_folder = "tests/"
Vote.database_folder = "tests/"

commands_db_path = Path(__file__).parent.parent.joinpath(Command.database_path)
users_db_path = Path(__file__).parent.parent.joinpath(User.database_path)
sfx_votes_db = Path(__file__).parent.parent.joinpath(SFXVote.database_path)
votes_db_path = Path(__file__).parent.parent.joinpath(Vote.database_path)
soundeffect_requests_db_path = Path(__file__).parent.parent.joinpath(
    SoundeffectRequest.database_path
)


class DatabaseConfig:
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        if commands_db_path.is_file():
            commands_db_path.unlink()
        if sfx_votes_db.is_file():
            sfx_votes_db.unlink()
        if users_db_path.is_file():
            users_db_path.unlink()
        if votes_db_path.is_file():
            votes_db_path.unlink()
        if soundeffect_requests_db_path.is_file():
            soundeffect_requests_db_path.unlink()
        yield
