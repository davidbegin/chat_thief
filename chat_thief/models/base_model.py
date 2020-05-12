from abc import ABC
import abc

from chat_thief.models.database import db_table

from tinydb import Query


class BaseModel(ABC):
    database_folder = ""

    def _update_value(self, field, amount=1):
        def _update_that_value():
            def transform(doc):
                doc[field] = doc[field] + amount

            return transform

        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.update_callable(_update_that_value(), Query().name == self.name)

    def _set_value(self, field, value):
        def _update_that_value():
            def transform(doc):
                doc[field] = value

            return transform

        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.update_callable(_update_that_value(), Query().name == self.name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def purge(cls):
        return cls.db().purge()

    # @abc.abstractmethod
    # def doc(self):
    #     """The dict representation of the model"""
    #     return
