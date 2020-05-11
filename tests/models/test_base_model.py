import pytest

from chat_thief.models.base_model import BaseModel

from tests.support.database_setup import DatabaseConfig


class TestBaseModel(DatabaseConfig):
    def test_save(self):
        pass
