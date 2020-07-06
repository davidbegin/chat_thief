import abc
import itertools
import operator
from typing import Callable

from tinydb import Query  # type: ignore

from chat_thief.models.transaction import transaction
from chat_thief.models.database import db_table


class BaseDbModel(abc.ABC):
    database_folder = ""

    @classmethod
    def count_by_group(cls, category):
        all_data = cls.db().all()

        def get_by_category(item):
            return item.get(category)

        grouped_data = itertools.groupby(
            sorted(all_data, key=get_by_category), get_by_category
        )

        data_counts = [(category, len(list(data))) for (category, data) in grouped_data]
        return list(reversed(sorted(data_counts, key=lambda data: data[1])))

    @classmethod
    def delete(cls, doc_ids):
        if not isinstance(doc_ids, list):
            doc_ids = [doc_ids]
        return cls.db().remove(doc_ids=doc_ids)

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
        return cls.db().truncate()

    @classmethod
    def truncate(cls):
        return cls.db().truncate()

    @classmethod
    def set_value_by_id(cls, doc_id, field, value):
        def _update_that_value():
            def transform(doc):
                doc[field] = value

            return transform

        with transaction(cls.db()) as tr:
            # db.update(your_operation(arguments), query)
            tr.update(_update_that_value(), doc_ids=[doc_id])

    @abc.abstractmethod
    def doc(self):
        """The dict representation of the model"""
        return

    # this is always based on the name, you should be able to override
    def set_value(self, field, value) -> None:
        def _update_that_value():
            def transform(doc):
                doc[field] = value

            return transform

        with transaction(self.db()) as tr:
            tr.update(_update_that_value(), Query().name == self.name)

    def update(self, update_func: Callable):
        with transaction(self.db()) as tr:
            return tr.update(update_func(), Query().name == self.name)
        return self

    def save(self) -> 'BaseDbModel':
        with transaction(self.db()) as tr:
            tr.insert(self.doc())
        return self

    def update_value(self, field: str, amount: int = 1) -> None:
        self._update_value(field, amount=1)

    def _update_value(self, field: str, amount: int = 1) -> None:
        def _update_that_value():
            def transform(doc):
                if field in doc:
                    doc[field] = doc[field] + amount
                else:
                    doc[field] = amount

            return transform

        with transaction(self.db()) as tr:
            tr.update(_update_that_value(), Query().name == self.name)
