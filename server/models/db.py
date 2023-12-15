from pydantic import BaseModel
from typing import ClassVar
import dataset

db = dataset.connect("sqlite:///:memory:")


class ModelMeta(type(BaseModel)):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._table = db[name]


class TableDescriptor:
    class TableWithParsing:
        def __init__(self, table, owner):
            self.table = table
            self.owner = owner

        def __getattr__(self, name):
            attr = getattr(self.table, name)
            print(name)
            if callable(attr):

                def wrapper(*args, **kwargs):
                    records = attr(*args, **kwargs)
                    if isinstance(records, dataset.util.ResultIter):
                        return [self.owner(**record) for record in records]
                    elif isinstance(records, dict):
                        return self.owner(**records)
                    else:
                        return records

                return wrapper
            else:
                return attr

    def __get__(self, _, owner) -> dataset.Table:
        return self.TableWithParsing(owner._table, owner)


class Model(BaseModel, metaclass=ModelMeta):
    """A Pydantic model that is backed by a dataset table.

    This class is a Pydantic model that is backed by a dataset table. It
    provides a descriptor that allows the dataset table to be accessed
    directly from the class, and it also provides a custom `__init__`
    method that allows the model to be initialized from a dataset record.
    """
    _table: dataset.Table = None
    objects: ClassVar[dataset.Table] = TableDescriptor()

    def save(self):
        """Save the model to the database.

        This method saves the model to the database. If the model already
        exists in the database, it will be updated. Otherwise, it will be
        inserted.
        """
        self._table.upsert(self.model_dump(), ["id"])
