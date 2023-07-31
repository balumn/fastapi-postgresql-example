from typing import Any

import inflect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker

from app.config import settings


Base = declarative_base()
SQLALCHEMY_DATABASE_URL = settings.assemble_db_connection()
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

p = inflect.engine()


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically in plural form.
    # i.e 'Store' model will generate table name 'stores'
    @declared_attr
    def __tablename__(cls) -> str:
        return p.plural(cls.__name__.lower())
