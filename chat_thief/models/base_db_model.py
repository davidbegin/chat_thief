import abc

from tinydb import Query

from chat_thief.models.database import db_table


class BaseDbModel(abc.ABC):
    database_folder = ""

    @classmethod
    def delete(cls, doc_id):
        return cls.db().remove(doc_ids=[doc_id])

    @classmethod
    def count(cls):
        return len(cls.all())

    @classmethod
    def all(cls):
        return cls.db().all()

    @classmethod
    def last(cls):
        # How do I grab the last with Tiny DB
        if cls.all():
            return cls.all()[-1]

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def purge(cls):
        return cls.db().purge()

    @abc.abstractmethod
    def doc(self):
        """The dict representation of the model"""
        return

    # this is always based on the name, you should be able to override
    def set_value(self, field, value):
        def _update_that_value():
            def transform(doc):
                doc[field] = value

            return transform

        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.update_callable(_update_that_value(), Query().name == self.name)

    def save(self):
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(self.doc())
