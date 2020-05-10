from tinydb import Query


class BaseModel:
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
