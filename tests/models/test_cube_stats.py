from pathlib import Path

import pytest

from chat_thief.models.user import User
from chat_thief.models.cube_stats import CubeStats


from tests.support.database_setup import DatabaseConfig


class TestCubeStats(DatabaseConfig):
    def test_stats
