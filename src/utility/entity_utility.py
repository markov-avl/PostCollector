from typing import final

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Relationship

from src.database.entity import Entity


@final
class EntityUtility:

    @staticmethod
    def foreign_key(entity: type[Entity], on_delete: str = "CASCADE", on_update: str = "CASCADE") -> ForeignKey:
        return ForeignKey(f'{entity.__tablename__}.{entity.id.key}', ondelete=on_delete, onupdate=on_update)

    @staticmethod
    def relationship[E](entity: type[E], lazy: str = "selectin") -> Relationship[E]:
        return relationship(entity, lazy=lazy)
