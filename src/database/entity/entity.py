from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative, Mapped


@as_declarative()
class Entity:
    __tablename__: str

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        attrs = (f"{c.name}={repr(getattr(self, c.name))}" for c in self.__class__.__dict__["__table__"].columns[::-1])
        return f"{self.__class__.__name__}({', '.join(attrs)})"
