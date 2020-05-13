import pytest

from pathlib import Path

from chat_thief.models.base_db_model import BaseDbModel

from tests.support.database_setup import DatabaseConfig


class FakeClass(BaseDbModel):
    pass


class RealFakeClass(BaseDbModel):
    database_folder = "tests/"
    database_path = "db/fake_things.json"
    table_name = "fake_things"

    def doc(self):
        return {"name": "thugga"}


MODEL_CLASSES = [RealFakeClass]


class TestBaseDbModel(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def destroy_db(self):
        for model in MODEL_CLASSES:
            db_path = Path(__file__).parent.parent.joinpath(model.database_path)
            if db_path.is_file():
                db_path.unlink()
        yield

    def test_class_without_doc(self):
        with pytest.raises(TypeError) as err_info:
            subject = FakeClass()

    def test_working_class(self):
        assert RealFakeClass.count() == 0
        subject = RealFakeClass()
        subject.save()
        assert RealFakeClass.count() == 1
        assert isinstance(RealFakeClass.all(), list)
        RealFakeClass.delete(1)
        assert RealFakeClass.count() == 0
