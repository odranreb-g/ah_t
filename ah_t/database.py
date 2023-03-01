from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ah_t.config import settings

engine = create_engine(settings.db_prod_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
