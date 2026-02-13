from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    # e.g., class User -> table "user" (or "users" if explicit)
    # This saves you from typing __tablename__ = "x" in every single model
    @declared_attr
    def __tablename__(cls) -> str:
    # This turns User -> users and IntegrityViolation -> integrityviolations
    # (Or just return cls.__name__.lower() + "s")
        return cls.__name__.lower() + "s"