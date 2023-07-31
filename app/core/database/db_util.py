from app.core.database.db import Base
from app.core.database.db import engine
from app.core.database.db import SessionLocal

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
