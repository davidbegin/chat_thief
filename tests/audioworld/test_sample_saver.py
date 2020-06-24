import pytest

from chat_thief.audioworld.sample_saver import SampleSaver
from chat_thief.models.command import Command

from tests.support.database_setup import DatabaseConfig


class TestSampleSaver(DatabaseConfig):
    def test_saving_a_sample(self):
        assert Command.count() == 0
        subject = SampleSaver(
            user="thugga",
            youtube_id="UZvwFztC1Gc",
            command="my_girlfriend",
            start_time="0:08",
            end_time="0:13",
        )
        subject.save()
        assert Command.count() == 1
        subject.save()
        assert Command.count() == 1

    def test_saving_a_problem_sample(self):
        assert Command.count() == 0
        subject = SampleSaver(
            user="qwertimer",
            youtube_id="https://www.youtube.com/watch?v=Ve-ATf6OTBQ",
            command="qwertimer",
            start_time="0:07",
            end_time="0:11",
        )
        subject.save()
        assert Command.count() == 1
